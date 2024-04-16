from util.json_handle import dict_get_or_panic

import json

import db_functional_service.rmq_handle as rmq


from crud.objects.customer_service import CustomerServiceCRUD
from crud.objects.customer import CustomerCRUD

import util.parse_env as ps

from util.reply_ctx import add_reply_ctx


def insert_customer(req_data, reply, srv_req_data):
    print("Enter insert_customer")

    # Check keys.
    required_keys = [
        "customer_id",
        "contact_info",
        "company_name",
        "black_list",
        "tags",
        "white_list",
        "specific_features",
        "services",
    ]

    data_dict = {}
    for key in required_keys:
        data_dict[key] = dict_get_or_panic(req_data, key, srv_req_data)

    # Insert customer.
    print("Insert customer")
    CustomerCRUD.insert_one({
        "customer_id": data_dict["customer_id"],
        "contact_info": data_dict["contact_info"],
        "company_name": data_dict["company_name"],
        "black_list": data_dict["black_list"],
        "tags": data_dict["tags"],
        "white_list": data_dict["white_list"],
        "specific_features": data_dict["specific_features"],
    })
    print("Finish insert customer")

    # Insert customer services.
    print("Insert customer services")
    for service in data_dict["services"]:
        service["customer_id"] = data_dict["customer_id"]

    CustomerServiceCRUD.insert_all(data_dict["services"])
    print("Finish insert customer services")
