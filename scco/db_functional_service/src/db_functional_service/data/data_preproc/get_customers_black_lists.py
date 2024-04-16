request_1 = {
    "request_name": "get_customers_black_lists",
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
            ]
        },
        {
            "customer_id": "customer_2",
            "black_list": [
                "bitch",
                "freak"
            ]
        }
    ],
    "reply_ctx": "something"
}
