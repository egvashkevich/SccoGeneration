import inspect

from util.json_handle import dict_get_or_panic
import crud.message_group_id_generator as mgig

from crud.models import NewQueriesCsv
from crud.type_map import CsvId

from crud.objects.query import QueryCRUD
from crud.objects.client import ClientCRUD
from crud.objects.new_queries_csv import NewQueriesCsvCRUD

import json

import db_functional_service.rmq_handle as rmq

import util.parse_env as ps

from util.reply_ctx import add_reply_ctx


def get_csv_id(req_data, srv_req_data) -> CsvId:
    print("Start get_csv_id")

    csv_path = dict_get_or_panic(req_data, "csv_path", srv_req_data)

    csv_ind = NewQueriesCsvCRUD.select_one(
        [NewQueriesCsv.csv_id],
        [NewQueriesCsv.csv_path == csv_path]
    )
    if csv_ind is None:
        raise RuntimeError(
            inspect.cleandoc(
                f"""
Passed csv_path is not presented in the database.
csv_path = {csv_path}
---------------------------------
srv_query_data = {json.dumps(srv_req_data, indent=2)}"""
                )
        )
    else:
        csv_ind = csv_ind[0]

    print(f"Finish get_csv_id"
          f"csv_file_ind = {csv_ind}")

    return csv_ind


def flatten_data_dict(arr_obj: dict) -> list[dict]:
    zip_obj = zip(
        arr_obj["channel_ids"],
        arr_obj["messages"],
        arr_obj["message_dates"],
    )

    res = []
    for chan, msg, date in zip_obj:
        res_item = {}
        for k, v in arr_obj.items():
            if k == "channel_ids":
                res_item["channel_id"] = chan
            elif k == "messages":
                res_item["message"] = msg
            elif k == "message_dates":
                res_item["message_date"] = date
            else:
                res_item[k] = v
        res.append(res_item)

    return res


def check_lens(data_dict, row, srv_req_data) -> None:
    ch_ids_len = len(data_dict["channel_ids"])
    msg_len = len(data_dict["messages"])
    msg_dates_len = len(data_dict["message_dates"])
    if msg_len != ch_ids_len or msg_len != msg_dates_len:
        RuntimeError(
            inspect.cleandoc(
                f"""
Length of channel_ids, messages and message_dates do not match.
---------------------------------
row = {json.dumps(row, indent=2)}
---------------------------------
srv_query_data = {json.dumps(srv_req_data, indent=2)}"""
                )
        )


def insert_message_group(data_dict, group_ids):
    print("Start insert_message_group")

    # Prepare data for insertion.
    group_id = mgig.IdGenerator.reserve_id()
    group_ids.append(group_id)

    insert_dicts = flatten_data_dict(data_dict)
    # print("HERE")
    for query_dict in insert_dicts:
        query_dict["csv_id"] = data_dict["csv_id"]
        query_dict["message_group_id"] = group_id

    # Insert new client.
    for query_dict in insert_dicts:
        if not ClientCRUD.contain(query_dict["client_id"]):
            print("Insert new client")
            ClientCRUD.insert_one(
                {
                    "client_id": query_dict["client_id"],
                    "attitude": "default"
                }
            )
            print("Insert new client finished")

    # Insert queries.
    QueryCRUD.insert_all(insert_dicts)

    print("insert_message_group finished")


def insert_preprocessed_queries(req_data, reply, srv_req_data):
    csv_path = dict_get_or_panic(req_data, "csv_path", srv_req_data)
    arr = dict_get_or_panic(req_data, "array_data", srv_req_data)

    # Check keys of array_data.
    required_keys = [
        "customer_id",
        "client_id",
        "channel_ids",
        "messages",
        "message_dates",
    ]

    csv_id = get_csv_id(req_data, srv_req_data)

    group_ids = []

    for row in arr:
        # Validate keys.
        data_dict = {}
        for key in required_keys:
            data_dict[key] = dict_get_or_panic(row, key, arr)

        check_lens(data_dict, row, srv_req_data)

        data_dict["csv_id"] = csv_id
        insert_message_group(data_dict, group_ids)

    answer = {
        "array_data": group_ids,
    }

    # Add reply_ctx.
    add_reply_ctx(srv_req_data, answer)

    # Send query to rabbitmq.
    answer = json.dumps(answer, indent=2)
    print(f"Answer:\n{answer}")

    if not ps.is_on_host():
        rmq.RmqHandle.basic_publish(answer, reply)
