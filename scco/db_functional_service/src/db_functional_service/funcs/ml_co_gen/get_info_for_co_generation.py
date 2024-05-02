import json
import inspect

from sqlalchemy import desc

from util.json_handle import dict_get_or_panic
from util.reply_ctx import add_reply_ctx

from crud.models import Query
from crud.models import Client
from crud.models import Customer
from crud.models import CustomerService

from crud.objects.query import QueryCRUD
from crud.objects.client import ClientCRUD
from crud.objects.customer import CustomerCRUD
from crud.objects.customer_service import CustomerServiceCRUD

from db_functional_service.reply import Reply
from db_functional_service.broker.broker import Broker


def arise_error(field_name, data_dict, query_data, db_query):
    raise RuntimeError(
        inspect.cleandoc(
            f"""
Unexpected error: no such {field_name} in table.
{field_name}: {data_dict[field_name]}
query_data: {json.dumps(query_data, indent=2)}
db_query: {json.dumps(db_query, indent=2)}"""
        )
    )


def get_from_query_table(data_dict, req_data, srv_req_data) -> dict:
    print("Start get_from_query_table")

    result_set = QueryCRUD.select_all(
        [
            Query.customer_id,
            Query.client_id,
            Query.channel_id,
            Query.message,
            # Query.message_date,
        ],
        wheres_cond=[
            Query.message_group_id == data_dict["message_group_id"],
        ],
        order_bys=[
            desc(Query.message_date),
        ],
    )
    print("QueryCRUD.select_all completed")

    if result_set is None or len(result_set) == 0:
        arise_error(
            "message_group_id",
            data_dict,
            req_data,
            srv_req_data
        )

    print(f"-----------------------------")
    print(f"result_set = {result_set}")
    print(f"-----------------------------")

    customer_id = result_set[0][0]
    client_id = result_set[0][1]
    channel_ids = []
    messages = []
    # messages_dates = []
    for row in result_set:
        channel_ids.append(row[2])
        messages.append(row[3])
        # messages_dates.append(row[4])

    answer = {
        "customer_id": customer_id,
        "client_id": client_id,
        "channel_ids": channel_ids,
        "messages": messages,
        # "message_dates": messages_dates,
    }

    return answer


def get_from_client_table(data_dict, req_data, srv_req_data) -> dict:
    print("Start get_from_client_table")

    result_set = ClientCRUD.select_one(
        [
            Client.attitude,
        ],
        wheres_cond=[
            Client.client_id == data_dict["client_id"],
        ],
    )
    print("ClientCRUD.select_one completed")

    if result_set is None:
        arise_error(
            "client_id",
            data_dict,
            req_data,
            srv_req_data
        )

    print(f"-----------------------------")
    print(f"result_set = {result_set}")
    print(f"-----------------------------")

    answer = {
        "attitude": result_set[0],
    }

    return answer


def get_from_customer_table(data_dict, req_data, srv_req_data) -> dict:
    print("Start get_from_customer_table")

    result_set = CustomerCRUD.select_one(
        [
            Customer.company_name,
            Customer.black_list,
            Customer.tags,
            Customer.white_list,
            Customer.specific_features,
        ],
        wheres_cond=[
            Customer.customer_id == data_dict["customer_id"],
        ],
    )
    print("CustomerCRUD.select_one completed")

    if result_set is None:
        arise_error(
            "customer_id",
            data_dict,
            req_data,
            srv_req_data,
        )

    print(f"-----------------------------")
    print(f"result_set = {result_set}")
    print(f"-----------------------------")

    answer = {
        "company_name": result_set[0],
        "black_list": result_set[1],
        "tags": result_set[2],
        "white_list": result_set[3],
        "specific_features": result_set[4],
    }

    return answer


def get_from_customer_service_table(
        data_dict,
        query_data,
        db_query) -> dict:
    print("Start get_from_customer_service_table")

    result_set = CustomerServiceCRUD.select_all(
        [
            CustomerService.service_name,
            CustomerService.service_desc,
        ],
        wheres_cond=[
            CustomerService.customer_id == data_dict["customer_id"],
        ],
    )
    print("CustomerServiceCRUD.select_all completed")

    if result_set is None:
        arise_error(
            "customer_id",
            data_dict,
            query_data,
            db_query,
        )

    print(f"-----------------------------")
    print(f"result_set = {result_set}")
    print(f"-----------------------------")

    services_list = []
    for row in result_set:
        services_list.append(
            {
                "service_name": row[0],
                "service_desc": row[1],
            }
        )

    answer = {
        "customer_services": services_list,
    }

    return answer


def get_info_for_co_generation(
        req_data,
        srv_req_data,
        reply: Reply,
        broker: Broker
) -> None:
    required_keys = [
        "message_group_id",
    ]

    # Validate keys.
    data_dict = {}
    for key in required_keys:
        data_dict[key] = dict_get_or_panic(req_data, key, srv_req_data)

    answer = {}

    # Query 1.
    answer_query = get_from_query_table(
        data_dict,
        req_data,
        srv_req_data,
    )
    answer.update(answer_query)
    data_dict["client_id"] = answer_query["client_id"]
    data_dict["customer_id"] = answer_query["customer_id"]

    # Query 2.
    answer_client = get_from_client_table(
        data_dict,
        req_data,
        srv_req_data,
    )
    answer.update(answer_client)

    # Query 3.
    answer_customer = get_from_customer_table(
        data_dict,
        req_data,
        srv_req_data,
    )
    answer.update(answer_customer)

    # Query 4.
    answer_customer_service = get_from_customer_service_table(
        data_dict,
        req_data,
        srv_req_data,
    )
    answer.update(answer_customer_service)

    print("Preparing answer")

    # Add reply_ctx.
    add_reply_ctx(srv_req_data, answer)

    # Send query to rabbitmq.
    answer = json.dumps(answer, indent=2)
    print(f"Answer:\n{answer}")

    print("sending reply")
    broker.basic_publish_unknown(
        reply.get_publisher(),
        answer.encode("utf-8"),
    )
