import os

from crud.objects.customer import CustomerCRUD
from crud.objects.customer_service import CustomerServiceCRUD

from testing.init_db import parse_customer

SERVICE_PKG_DIR = os.path.dirname(__file__)


def db_insert_on_first_startup() -> None:
    print("start db_insert_dummy_values")

    ############################################################################
    # Customer.

    customer_1, customer_1_services = parse_customer(
        f"{SERVICE_PKG_DIR}/data/init_db/customer_it.json"
    )
    customer_2, customer_2_services = parse_customer(
        f"{SERVICE_PKG_DIR}/data/init_db/customer_builder.json"
    )

    print("Start insert customers")
    CustomerCRUD.insert_all([
        customer_1,
        customer_2,
    ])
    print("Finished insert customers")

    ############################################################################
    # CustomerService.

    print("Start insert customer_service")
    CustomerServiceCRUD.insert_all([
        *customer_1_services,
        *customer_2_services,
    ])
    print("Finished insert customer_service")

    ############################################################################

    print("finished dummy_init_db")
