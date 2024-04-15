import pandas as pd
import json
import os
import pika
import sys
from abc import ABC, abstractmethod

import config
from tools.dict_occurrence import DictOccurrenceManager


class Operation(ABC):
    @abstractmethod
    def __call__(self, data):
        pass


class BlackList(ABC):
    @abstractmethod
    def load(self):
        pass


class StableSortBy(Operation):
    def __init__(self, column):
        self.column = column

    def __call__(self, data):
        return data.sort_values(self.column, kind='stable')


class GroupBy(Operation):
    def __init__(self, columns, agg=None):
        self.columns = columns
        self.agg = agg

    def __call__(self, data):
        return data.groupby(self.columns).agg(self.agg).reset_index()


class FilterAlreadySeen(Operation):
    def __init__(self, by, customer_id, on_nothing_left):
        self.by = by
        self.customer_id = customer_id
        self.on_nothing_left = on_nothing_left

    def __call__(self, data):
        query_data = []
        for index, row in data.iterrows():
            item = dict()
            for col in self.by:
                item[col] = row[col]
            item['customer_id'] = self.customer_id
            query_data.append(item)
        query = json.dumps({
            "query_name": "contains_query",
            "reply": {
                "exchange": config.CONTAINS_QUERY_EXCHANGE,
                "queue": "<generated queue name>",  # TODO
                "routing_key": config.CONTAINS_QUERY_ROUTING_KEY,
            },
            "query_data": query_data
        })
        print(query)  # TODO: send query
        result = data[self.by]
        return data.merge(result, how='right', on=self.by)


class FilterByBlackList(Operation):
    def __init__(self, black_list, on_nothing_left, errors_num=0):
        self.black_list = black_list
        self.on_nothing_left = on_nothing_left
        self.errors_num = errors_num

    def __call__(self, data):
        black_list = self.black_list.load()
        occurrence_manager = DictOccurrenceManager(black_list)

        if self.errors_num == 0:
            predicate = lambda s: not occurrence_manager.check_exact_occurrence(s)
        else:
            predicate = lambda s: not occurrence_manager.check_occurrence_with_errors(s, self.errors_num)

        return data[[predicate(s) for s in data['message']]]


class CommonBlackList(BlackList):
    def load(self):
        with open('resources/common_blacklist.txt', 'r') as f:
            common_black_list = {s.strip() for s in f.readlines()}
        if '' in common_black_list:
            common_black_list.remove('')
        return common_black_list


class CustomerBlackList(BlackList):
    def __init__(self, customer_id):
        self.customer_id = customer_id

    def load(self):
        query = json.dumps({
            "query_name": "black_list_query",
            "reply": {
                "exchange": config.BLACK_LIST_QUERY_EXCHANGE,
                "queue": "<generated queue name>",  # TODO
                "routing_key": config.BLACK_LIST_QUERY_ROUTING_KEY,
            },
            "query_data": {
                "customer_id": self.customer_id
            }
        })
        print(query)  # TODO: send query
        black_list = set()
        return black_list


class InsertToDatabase(Operation):
    def __init__(self, customer_id):
        self.customer_id = customer_id

    def __call__(self, data):
        new_data = data.rename(columns={'message': 'messages', 'message_date': 'message_dates'})
        query_data = []
        for index, row in new_data.iterrows():
            item = dict()
            for col in new_data.columns:
                item[col] = row[col]
            item['customer_id'] = self.customer_id
            query_data.append(item)
        query = json.dumps({
            "query_name": "insert_after_preprocessing_query",
            "reply": {
                "exchange": config.INSERT_AFTER_PREPROCESSING_QUERY_EXCHANGE,
                "queue": "<generated queue name>",  # TODO
                "routing_key": config.INSERT_AFTER_PREPROCESSING_QUERY_ROUTING_KEY,
            },
            "query_data": query_data
        })
        print(json.loads(query))  # TODO
        result = pd.DataFrame(data.index)
        return result
