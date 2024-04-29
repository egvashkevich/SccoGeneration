request_1 = {
    "request_name": "get_customers_lists",
    "reply": {
        "exchange": "scco_test_exchange",
        "routing_key": "scco_test_rk",
    },
    "reply_ctx": "something",  # not required
    "request_data": [
        {
            "customer_id": "customer_1",
        },
        {
            "customer_id": "customer_2",
        }
    ]
}

################################################################################

answer_1 = {
  "array_data": [
    {
      "customer_id": "customer_1",
      "black_list": [
        "fuck",
        "shit",
        "nigger"
      ],
      "white_list": [
        "python_synonym",
        "b2b_synonym"
      ]
    },
    {
      "customer_id": "customer_2",
      "black_list": [
        "bitch",
        "freak"
      ],
      "white_list": [
        "golang_synonym",
        "devops_synonym"
      ]
    }
  ],
  "reply_ctx": "something"
}
