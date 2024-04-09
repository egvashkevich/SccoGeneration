contains_query_request_1 = {
    "query_name": "contains_query",
    "reply": {
        "exchange": "test_exchange",
        "queue": "test_queue",
        "routing_key": "test_routing_key",
    },
    "query_data": [
        {
            "customer_id": "customer_1",
            "client_id": "client_1",
            "channel_id": "phystech.career",
            "message_date": "2024-01-01T00:00:00",
        },
        {
            "customer_id": "customer_1",
            "client_id": "client_2",
            "channel_id": "phystech.career",
            "message_date": "2023-12-31T23:59:00",
        }
    ]
}

################################################################################

contains_query_answer_1 = [
  {
    "customer_id": "customer_1",
    "client_id": "client_1",
    "channel_id": "phystech.career",
    "message_date": "2024-01-01 00:00:00"
  }
]
