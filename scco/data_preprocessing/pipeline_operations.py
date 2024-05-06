import numpy as np
import pandas as pd
import json
import os
import pika
import sys
import uuid
import datetime
from io import StringIO
from rabbit_rpc import FilterRpcClient, SaveCsvRpcClient
from abc import ABC, abstractmethod

import config
from tools.dict_occurrence import DictOccurrenceManager
from tools.pattern_text_matching import Matcher


class Operation(ABC):
    @abstractmethod
    def __call__(self, data):
        pass


class MatchingList(ABC):
    @abstractmethod
    def load(self):
        pass


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

        # TODO insert_csv_path_do_db(new_queries_csv_path)


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
            matcher = Matcher()

            def any_match(s):
                for pattern in matching_list:
                    print(f'Debug: search {pattern=} in {s=} with matcher:',
                          matcher.count_matches(pattern, s), flush=True)
                    print(f'Debug: search {pattern=} in {s=} with in:', pattern in s, flush=True)
                    if pattern in s:  # matcher.count_matches(pattern, s) > 0:
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


# class FilterByBlackList(Operation):
#     def __init__(self, black_list, on_nothing_left, errors_num=0):
#         self.black_list = black_list
#         self.on_nothing_left = on_nothing_left
#         self.errors_num = errors_num

#     def __call__(self, data):
#         black_list = self.black_list.load()
#         occurrence_manager = DictOccurrenceManager(black_list)

#         if self.errors_num < 0:
#             predicate = lambda s: not occurrence_manager.check_occurence_adaptive(s)
#         elif self.errors_num == 0:
#             predicate = lambda s: not occurrence_manager.check_exact_occurrence(s)
#         else:
#             predicate = lambda s: not occurrence_manager.check_occurrence_with_errors(s, self.errors_num)

#         return data[[predicate(s) for s in data['message']]]


class CommonMatchingList(MatchingList):
    def __init__(self, path='resources/common_blacklist.txt'):
        self.path = path

    def load(self):
        with open(self.path, 'r') as f:
            common_matching_list = {s.strip() for s in f.readlines()}
        if '' in common_matching_list:
            common_matching_list.remove('')
        return common_matching_list


# class CustomerMatchingList(BlackList):
#     def __init__(self, customer_id):
#         self.customer_id = customer_id

#     def load(self):
#         query = json.dumps({
#             "query_name": "black_list_query",
#             "reply": {
#                 "exchange": config.BLACK_LIST_QUERY_EXCHANGE,
#                 "queue": "<generated queue name>",  # TODO
#                 "routing_key": config.BLACK_LIST_QUERY_ROUTING_KEY,
#             },
#             "query_data": {
#                 "customer_id": self.customer_id
#             }
#         })
#         print(query)  # TODO: send query
#         black_list = set()
#         return black_list


class InsertToDatabase(Operation):
    def __init__(self, customer_id, new_queries_csv):
        self.customer_id = customer_id
        self.new_queries_csv = new_queries_csv

    def __call__(self, data):
        items = []
        for index, row in data.iterrows():
            item = dict()
            for col in data.columns:
                item[col] = row[col]
            item['customer_id'] = self.customer_id
            items.append(item)
        query = json.dumps({
            "query_name": "insert_after_preprocessing_query",
            "reply": {
                "exchange": config.INSERT_AFTER_PREPROCESSING_QUERY_EXCHANGE,
                "queue": "<generated queue name>",  # TODO
                "routing_key": config.INSERT_AFTER_PREPROCESSING_QUERY_ROUTING_KEY,
            },
            "query_data": {
                "csv_path": self.new_queries_csv,
                "array_data": items
            }
        })
        print(json.loads(query))  # TODO
        result = pd.DataFrame(data.index)
        return result
