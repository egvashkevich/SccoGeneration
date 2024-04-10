insert_offers_request_1 = {
    "query_name": "insert_offers",
    "reply": {
        "exchange": "test_exchange",
        "routing_key": "test_routing_key",
    },
    "query_data": [
        {
            "message_group_id": "1",
            "file": "/path/to/offer1",
        },
        {
            "message_group_id": "2",
            "file": "/path/to/offer2",
        },
    ]
}

################################################################################

insert_offers_answer_1 = [
  {
    "customer_id": "customer_1",
    "client_id": "client_1",
    "file": "/path/to/offer1"
  },
  {
    "customer_id": "customer_2",
    "client_id": "client_2",
    "file": "/path/to/offer2"
  }
]
