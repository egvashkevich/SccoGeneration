import numpy as np
import pandas as pd
import json
import os
import uuid
import datetime
from abc import ABC, abstractmethod
from emoji import replace_emoji
from io import StringIO

import config
from rabbit_rpc import FilterRpcClient, SaveCsvRpcClient, MatchingListsRpcClient, InsertToDbRpcClient
from tools.dict_occurrence import DictOccurrenceManager
# from tools.pattern_text_matching import Matcher


class Operation(ABC):
    @abstractmethod
    def __call__(self, data: pd.DataFrame) -> pd.DataFrame:
        pass


class PreprocessingPipeline:
    def __init__(self,
                 customer_id,
                 new_queries_csv_info,  # TODO lifecycle
                 filter_rpc_client: FilterRpcClient,
                 save_csv_rpc_client: SaveCsvRpcClient,
                 matching_lists_rpc_client: MatchingListsRpcClient,
                 insert_to_db_rpc_client: InsertToDbRpcClient):
        self.pipeline = [
            ColumnTransform('message', lambda s: replace_emoji(s, '')),
            ColumnTransform('message', str.lower),

            StableSortBy('message_date'),
            GroupBy(['channel_id', 'client_id', 'message_date'], agg={'message': (lambda x: list(x)[-1])}),
            FilterAlreadySeen(by=['channel_id', 'client_id', 'message_date'],
                              customer_id=customer_id, on_nothing_left='all messages were already seen',
                              rpc_client=filter_rpc_client),
            SaveNewQueries(new_queries_csv_info, save_csv_rpc_client),

            FilterByTextMatch(CommonMatchingList(), mode='blacklist', algorithm='word',
                              on_nothing_left='all messages filtered out by common black list'),

            FilterByTextMatch(CommonMatchingList('resources/trusted_strong_blacklist'), mode='blacklist',
                              on_nothing_left='all messages filtered out by common strong black list'),
            # FilterByTextMatch(CommonMatchingList('resources/trusted_strong_whitelist'), mode='whitelist',
            #                   on_nothing_left='all messages filtered out by common strong white list'),

            FilterByTextMatch(CommonMatchingList('resources/trusted_weak_whitelist'), mode='whitelist',
                              on_nothing_left='all messages filtered out by common weak white list'),
            FilterByTextMatch(CommonMatchingList('resources/trusted_weak_blacklist'), mode='blacklist',
                              on_nothing_left='all messages filtered out by common weak black list'),

            # order of these two matters, see MatchingListsRpcClient
            FilterByTextMatch(CustomerBlackList(customer_id, matching_lists_rpc_client), mode='blacklist',
                              on_nothing_left='all messages filtered out by customer\'s black list'),
            FilterByTextMatch(CustomerWhiteList(customer_id, matching_lists_rpc_client), mode='whitelist',
                              on_nothing_left='all messages filtered out by customer\'s white list'),

            GroupBy(['client_id'], agg={'channel_id': list, 'message': list, 'message_date': list},
                    rename={'channel_id': 'channel_ids', 'message': 'messages', 'message_date': 'message_dates'}),
            InsertToDatabase(customer_id, insert_to_db_rpc_client, new_queries_csv_info)
        ]

    def __call__(self, data):
        print(" [x] Data before pipeline:")
        print(data, flush=True)
        for operation in self.pipeline:
            data = operation(data)
            print(f" [x] Data after operation {type(operation)}:")
            print(data, flush=True)
            if data.empty:
                if hasattr(operation, 'on_nothing_left'):
                    print(' [x] Nothing to send further:', operation.on_nothing_left, flush=True)
                    break
                else:
                    raise ValueError('Nothing to send further, for an unpredicted reason')
        return data


class ColumnTransform(Operation):
    def __init__(self, column, function):
        self.column = column
        self.function = function

    def __call__(self, data):
        data[self.column] = data[self.column].map(self.function)
        return data


class StableSortBy(Operation):
    def __init__(self, column):
        self.column = column

    def __call__(self, data):
        return data.sort_values(self.column, kind='stable')


class GroupBy(Operation):
    def __init__(self, columns, agg=None, rename=None):
        self.columns = columns
        self.agg = agg
        self.rename = rename

    def __call__(self, data):
        result = data.groupby(self.columns).agg(self.agg).reset_index()
        if self.rename:
            result.rename(columns=self.rename)
        return result


class FilterAlreadySeen(Operation):
    def __init__(self, by, customer_id, on_nothing_left, rpc_client: FilterRpcClient):
        self.by = by
        self.customer_id = customer_id
        self.on_nothing_left = on_nothing_left
        self.rpc_client = rpc_client

    def __call__(self, data):
        request_data = []
        for index, row in data.iterrows():
            item = dict()
            for col in self.by:
                item[col] = row[col]
            item['customer_id'] = self.customer_id
            request_data.append(item)
        response = self.rpc_client.call(request_data)  # json-like object -> json-like object
        result = pd.read_json(StringIO(json.dumps(response)), orient='records')
        return data.merge(result, how='right', on=self.by)


class SaveNewQueries:
    def __init__(self, new_queries_csv_info, rpc_client: SaveCsvRpcClient):
        self.new_queries_csv_info = new_queries_csv_info
        self.rpc_client = rpc_client

    def __call__(self, data):
        today = datetime.date.today().strftime('%y-%m-%y')  # yyyy-mm-dd
        unique_id = uuid.uuid4().hex  # unique sting of hex symbols
        new_queries_csv_name = f'new-queries-{today}-{unique_id}.csv'

        os.makedirs(config.NEW_QUERIES_CSV_FOLDER, exist_ok=True)
        data.to_csv(os.path.join(config.NEW_QUERIES_CSV_FOLDER, new_queries_csv_name))

        new_queries_csv_path = config.NEW_QUERIES_PREFIX_FOR_SENDING + new_queries_csv_name
        self.new_queries_csv_info['path'] = new_queries_csv_path

        _ = self.rpc_client.call()

        return data


class FilterByTextMatch(Operation):
    def __init__(self, matching_list, mode, on_nothing_left, algorithm='substring'):
        self.matching_list = matching_list
        self.mode = mode
        self.algorithm = algorithm
        self.on_nothing_left = on_nothing_left

    def __call__(self, data):
        matching_list = self.matching_list.load()

        if self.algorithm == 'word':
            occurrence_manager = DictOccurrenceManager(matching_list)

            def any_match(s):
                return occurrence_manager.check_exact_occurrence(s)

        elif self.algorithm == 'substring':
            # matcher = Matcher()

            def any_match(s):
                for pattern in matching_list:
                    # print(f'Debug: search {pattern=} in {s=} with matcher:',
                    #       matcher.count_matches(pattern, s), flush=True)
                    # print(f'Debug: search {pattern=} in {s=} with in:', pattern in s, flush=True)
                    if pattern in s:  # TODO: matcher.count_matches(pattern, s) > 0:
                        return True
                return False

        else:
            raise ValueError(f'Unknown algorithm for FilterByTextMatch: {self.algorithm}')

        print(f' [x] Matching with {self.mode}', flush=True)
        mask = np.empty(len(data), dtype=bool)
        for i, s in enumerate(data['message']):
            if i % 20 == 0:
                print(f"{i} lines processed", flush=True)
            mask[i] = any_match(s)

        if self.mode == 'blacklist':
            return data[np.logical_not(mask)]
        elif self.mode == 'whitelist':
            return data[mask]
        else:
            raise ValueError(f'Unknown mode for FilterByTextMatch: {self.mode}')


class MatchingList(ABC):
    @abstractmethod
    def load(self):
        pass


class CommonMatchingList(MatchingList):
    def __init__(self, path='resources/common_blacklist.txt'):
        self.path = path

    def load(self):
        with open(self.path, 'r') as f:
            common_matching_list = {s.strip() for s in f.readlines()}
        if '' in common_matching_list:
            common_matching_list.remove('')
        return common_matching_list


class CustomerBlackList(MatchingList):
    def __init__(self, customer_id, rpc_client: MatchingListsRpcClient):
        self.customer_id = customer_id
        self.rpc_client = rpc_client

    def load(self):
        return set(self.rpc_client.get_black_list(self.customer_id))


class CustomerWhiteList(MatchingList):
    def __init__(self, customer_id, rpc_client: MatchingListsRpcClient):
        self.customer_id = customer_id
        self.rpc_client = rpc_client

    def load(self):
        return set(self.rpc_client.get_white_list(self.customer_id))


class InsertToDatabase(Operation):
    def __init__(self, customer_id, insert_to_db_rpc_client, new_queries_csv_info):
        self.customer_id = customer_id
        self.insert_to_db_rpc_client = insert_to_db_rpc_client
        self.new_queries_csv_info = new_queries_csv_info

    def __call__(self, data):
        items = []
        for index, row in data.iterrows():
            item = dict()
            for col in data.columns:
                item[col] = row[col]
            item['customer_id'] = self.customer_id
            items.append(item)
        response = self.insert_to_db_rpc_client.call(items)
        result = pd.DataFrame({'group_id': response})  # TODO
        return result
