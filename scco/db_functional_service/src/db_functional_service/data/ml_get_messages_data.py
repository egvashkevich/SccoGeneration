ml_get_messages_request_1 = {
    "query_name": "ml_get_messages",
    "reply": {
        "exchange": "test_exchange",
        "queue": "test_queue",
        "routing_key": "test_routing_key",
    },
    "query_data": {
            "message_group_id": "1",
    }
}

################################################################################

ml_get_messages_answer_1 = {
  "customer_id": "customer_1",
  "client_id": "client_1",
  "messages": [
    "Good morning.\nMy name is client_1.\nI need Python developers."
  ],
  "history": []
}
