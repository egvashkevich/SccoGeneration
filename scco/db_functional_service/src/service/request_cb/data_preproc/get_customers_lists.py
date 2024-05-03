from util.app_errors import dict_get_or_panic

from crud.models import Customer
from crud.objects.customer import CustomerCRUD

from service.request_cb.request_cb import RequestCallback


class GetCustomersLists(RequestCallback):
    def __init__(self):
        super().__init__()

    def make_call(
            self,
            req_data,
            srv_req_data,
    ) -> any:
        print("Enter GetCustomersLists callback")

        # Check keys.
        required_keys = [
            "customer_id",
        ]

        customer_ids = []

        for row in req_data:
            for key in required_keys:
                customer_ids.append(dict_get_or_panic(row, key, srv_req_data))

        # Make db query.
        print("Start query")
        result_set = CustomerCRUD.select_all(
            [
                Customer.customer_id,
                Customer.black_list,
                Customer.white_list,
            ],
            wheres_cond=[
                Customer.customer_id.in_(customer_ids),
            ],
        )

        print("Collecting data")
        answer_list = []
        for row in result_set:
            answer_list.append(
                {
                    "customer_id": row[0],
                    "black_list": row[1],
                    "white_list": row[2],
                }
            )

        print("Preparing answer")
        answer = {
            "array_data": answer_list,
        }
        return answer
