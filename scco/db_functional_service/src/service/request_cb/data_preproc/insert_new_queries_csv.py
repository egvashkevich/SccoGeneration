from util.app_errors import dict_get_or_panic

from crud.objects.new_queries_csv import NewQueriesCsvCRUD

from service.request_cb.request_cb import RequestCallback


class InsertNewQueriesCsv(RequestCallback):
    def __init__(self):
        super().__init__()

    def make_call(
            self,
            req_data,
            srv_req_data,
    ) -> any:
        print("Enter InsertNewQueriesCsv callback")

        # Check keys.
        required_keys = [
            "csv_path",
        ]

        data_dict = {}
        for key in required_keys:
            data_dict[key] = dict_get_or_panic(req_data, key, srv_req_data)

        # Make db query.
        print("Start query")
        NewQueriesCsvCRUD.insert_one(
            {
                "csv_path": data_dict["csv_path"],
            }
        )

        print("Preparing answer")
        answer = {
            "csv_path": data_dict["csv_path"],
        }
        return answer
