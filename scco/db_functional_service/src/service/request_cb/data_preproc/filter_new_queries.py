import datetime

from sqlalchemy import tuple_

import util.app_config as app_cfg

from util.app_errors import dict_has_or_panic
from util.app_errors import check_req_data_is_array
from util.app_errors import check_req_data_array_empty

from crud.models import Query
from crud.objects.query import QueryCRUD

from service.request_cb.request_cb import RequestCallback


class FilterNewQueries(RequestCallback):
    def __init__(self):
        super().__init__()

    def make_call(
            self,
            req_data,
            srv_req_data,
    ) -> any:
        print("Enter FilterNewQueries callback")

        if not check_req_data_is_array(req_data, srv_req_data) \
                or check_req_data_array_empty(req_data, srv_req_data):
            print("Exit without sending answer")
            return

        # Check keys.
        required_keys = [
            "customer_id",
            "client_id",
            "channel_id",
            "message_date",
        ]

        for row in req_data:
            for key in required_keys:
                dict_has_or_panic(row, key, srv_req_data)

        req_dict = {}
        for row in req_data:
            req_dict[get_sort_key(row, required_keys)] = row

        # Make db query.
        print("Creating query")
        columns = [
            Query.customer_id,
            Query.client_id,
            Query.channel_id,
            Query.message_date,
        ]
        tup = tuple_(*columns)
        tup.in_(req_dict.keys())

        print("Start query")
        result_set = QueryCRUD.select_all(
            columns=columns,
            wheres_cond=[
                tup.in_(req_dict.keys())
            ],
        )
        print(f"result_set:\n{result_set}")

        print("Process result_set")
        res_dict = dict(req_dict)
        for row in result_set:
            print(f"row.customer_id = {row.customer_id}")
            del res_dict[get_sort_key_row(row, required_keys)]

        res = list(res_dict.values())

        print("Preparing answer")
        answer = {
            "not_exist": res,
        }
        return answer

################################################################################

# Helpers


def get_sort_key(row, required_keys):
    res_list = []
    for key in required_keys:
        res_list.append(row[key])
    return tuple(res_list)


def get_sort_key_row(row, required_keys):
    res_list = []

    for key in required_keys:
        field = row.__getattribute__(key)
        if isinstance(field, datetime.datetime):
            field = field.strftime(app_cfg.DATETIME_FORMAT)
        res_list.append(field)

    return tuple(res_list)
