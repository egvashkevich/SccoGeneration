from util.app_errors import dict_get_or_panic

from crud.objects.customer_service import CustomerServiceCRUD
from crud.objects.customer import CustomerCRUD
from crud.models import Customer
from crud.models import CustomerService

from service.request_cb.request_cb import RequestCallback


class InsertCustomer(RequestCallback):
    def __init__(self):
        super().__init__()

    def make_call(
            self,
            req_data,
            srv_req_data,
    ) -> any:
        print("Enter InsertCustomer callback")

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

        # Check for customer to exist.
        result_one = CustomerCRUD.select_one(
            columns=[
                Customer.customer_id
            ],
            wheres_cond=[
                Customer.customer_id == data_dict["customer_id"],
            ]
        )

        if result_one is not None:
            # Customer already exists, updating him.
            print("Updating customer")
            CustomerCRUD.update(
                new_vals={
                    "contact_info": data_dict["contact_info"],
                    "company_name": data_dict["company_name"],
                    "black_list": data_dict["black_list"],
                    "tags": data_dict["tags"],
                    "white_list": data_dict["white_list"],
                    "specific_features": data_dict["specific_features"],
                },
                wheres_cond=[
                    Customer.customer_id == data_dict["customer_id"],
                ],
            )
            print("Finished updating customer")

            # Updating customer services.
            print("Deleting previous customer services")
            CustomerServiceCRUD.delete(
                wheres_cond=[
                    CustomerService.customer_id == data_dict["customer_id"],
                ],
            )
            print("Finished deleting previous customer services")

            for service in data_dict["services"]:
                service["customer_id"] = data_dict["customer_id"]

            print("Inserting new customer services")
            CustomerServiceCRUD.insert_all(data_dict["services"])
            print("Finished inserting customer services")

        else:
            # Customer not found, here is the new one.
            print("Inserting customer")
            CustomerCRUD.insert_one(
                {
                    "customer_id": data_dict["customer_id"],
                    "contact_info": data_dict["contact_info"],
                    "company_name": data_dict["company_name"],
                    "black_list": data_dict["black_list"],
                    "tags": data_dict["tags"],
                    "white_list": data_dict["white_list"],
                    "specific_features": data_dict["specific_features"],
                }
            )
            print("Finished inserting customer")

            # Insert customer services.
            print("Inserting customer services")
            for service in data_dict["services"]:
                service["customer_id"] = data_dict["customer_id"]

            CustomerServiceCRUD.insert_all(data_dict["services"])
            print("Finish insert customer services")
