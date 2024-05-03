import inspect
import datetime

import crud.message_group_id_generator as mgig

from crud.objects.customer import CustomerCRUD
from crud.objects.customer_service import CustomerServiceCRUD
from crud.objects.client import ClientCRUD
from crud.objects.new_queries_csv import NewQueriesCsvCRUD
from crud.objects.query import QueryCRUD
from crud.objects.offer import OfferCRUD

import util.app_config as app_cfg


def dummy_init_db() -> None:
    print("start insert_dummy_values")

    ############################################################################
    # Customer.
    customer_1 = {
        "customer_id": "customer_1",
        "contact_info": "telegram_link",
        "company_name": "Company of customer 1",
        "black_list": ["fuck", "shit", "nigger"],
        "tags": ["python", "b2b"],
        "white_list": ["python_synonym", "b2b_synonym"],
        "specific_features": ["feature_1", "feature_2"],
    }
    customer_2 = {
        "customer_id": "customer_2",
        "contact_info": "whatsapp_link",
        "company_name": "Company of customer 2",
        "black_list": ["bitch", "freak"],
        "tags": ["golang", "devops"],
        "white_list": ["golang_synonym", "devops_synonym"],
        "specific_features": ["feature_1", "feature_2"],
    }
    print("Start insert customers")
    CustomerCRUD.insert_all([customer_1, customer_2])
    print("Finished insert customers")

    ############################################################################
    # CustomerService.
    customer_services = [
        {
            "customer_id": "customer_1",
            "service_name": "customer 1, service 1",
            "service_desc": "description 1",
        },
        {
            "customer_id": "customer_1",
            "service_name": "customer 1, service 2",
            "service_desc": "description 2",
        },
        {
            "customer_id": "customer_2",
            "service_name": "customer 2, service 1",
            "service_desc": "description 1",
        }
    ]
    print("Start insert customer_services")
    CustomerServiceCRUD.insert_all(customer_services)
    print("Finished insert customer_services")

    ############################################################################
    # Client.
    client_1 = {
        "client_id": "client_1",
        "attitude": "arrogant",
    }
    client_2 = {
        "client_id": "client_2",
        "attitude": "famous",
    }
    print("Start insert clients")
    ClientCRUD.insert_all([client_1, client_2])
    print("Finished insert clients")

    ############################################################################
    # NewQueriesCsv.
    new_queries_csv_1 = {
        "csv_path": "path/to/new_queries1.csv",
    }
    new_queries_csv_2 = {
        "csv_path": "path/to/new_queries2.csv",
    }
    print("Start insert new_queries_csv")
    csv_ids = NewQueriesCsvCRUD.insert_all([new_queries_csv_1, new_queries_csv_2])
    print("Finished insert new_queries_csv")

    ############################################################################
    # Query.
    query_1 = {
        # "query_id": auto,
        "customer_id": customer_1["customer_id"],
        "client_id": client_1["client_id"],
        "csv_id": csv_ids[0],
        "channel_id": "phystech.career",
        "message": inspect.cleandoc("""Good morning.
            My name is client_1.
            I need Python developers."""),
        "message_group_id": mgig.IdGenerator.reserve_id(),
        "message_date": datetime.datetime.strptime(
                "2023-12-31T22:59:00",
                app_cfg.DATETIME_FORMAT
        ),
    }
    query_2 = {
        "customer_id": customer_1["customer_id"],
        "client_id": client_2["client_id"],
        "csv_id": csv_ids[1],
        "channel_id": "phystech.career",
        "message": inspect.cleandoc("""Hi!
            My name is client_2.
            I need C++ developers."""),
        "message_group_id": mgig.IdGenerator.reserve_id(),
        "message_date": datetime.datetime.strptime(
                "2023-12-31T23:59:00",
                app_cfg.DATETIME_FORMAT
        ),
    }
    print("Start insert queries")
    query_id_list = QueryCRUD.insert_all([query_1, query_2])
    print("Finished insert queries")

    ############################################################################
    # Offer.
    offer_1 = {
        "query_id": query_id_list[0],
        "file_path": "/path/to/offer1.pdf",
    }
    # offer_2 = {
    #     "query_id": query_id_list[1],
    #     "file": "/path/to/offer2",
    # }
    print("Start insert offers")
    OfferCRUD.insert_all([offer_1])
    # OfferCRUD.insert_all([offer_1, offer_2])
    print("Finished insert offers")

    ############################################################################

    print("finished insert_dummy_values")
