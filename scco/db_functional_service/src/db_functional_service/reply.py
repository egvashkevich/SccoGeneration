from db_functional_service.broker.broker import Publisher
from util.json_handle import dict_get_or_panic


class Reply:
    def __init__(self, srv_req_data: dict):
        if "reply" not in srv_req_data:
            self._not_required = True
            return
        else:
            self._not_required = False

        reply = srv_req_data["reply"]
        self._exchange = dict_get_or_panic(reply, "exchange", srv_req_data)
        self._routing_key = dict_get_or_panic(reply, "routing_key", srv_req_data)

    def is_required(self) -> bool:
        return self._not_required

    def get_publisher(self) -> Publisher:
        return Publisher(
            name="",  # not used
            exchange=self._exchange,
            queue="",  # not used
            routing_key=self._routing_key,
        )

