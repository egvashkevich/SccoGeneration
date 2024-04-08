get_black_list_request_1 = {
    "query_name": "get_black_list",
    "reply": {
        "exchange": "test_exchange",
        "queue": "test_queue",
        "routing_key": "test_routing_key",
    },
    "query_data": [
        {
            "customer_id": "customer_1",
        },
        {
            "customer_id": "customer_2",
        }
    ]
}

################################################################################

get_black_list_answer_1 = [
  {
    "customer_id": "customer_1",
    "black_list": [
      "fuck",
      "shit",
      "nigger"
    ]
  },
  {
    "customer_id": "customer_2",
    "black_list": [
      "bitch",
      "freak"
    ]
  }
]
