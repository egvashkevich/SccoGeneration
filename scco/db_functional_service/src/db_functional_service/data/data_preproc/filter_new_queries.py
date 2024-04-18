request_1 = {
    "request_name": "filter_new_queries",
    "reply": {
        "exchange": "scco_test_exchange",
        "routing_key": "scco_test_rk",
    },
    "reply_ctx": "something",  # not required
    "request_data": [
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

answer_1 = {
  "not_exist": [
    {
      "customer_id": "customer_1",
      "client_id": "client_1",
      "channel_id": "phystech.career",
      "message_date": "2024-01-01T00:00:00"
    }
  ],
  "reply_ctx": "something"
}
