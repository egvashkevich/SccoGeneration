request_1 = {
    "request_name": "get_info_for_co_generation",
    "reply": {
        "exchange": "scco_test_exchange",
        "routing_key": "scco_test_routing_key",
    },
    "reply_ctx": "something",  # not required
    "request_data": {
        "message_group_id": "1",
    }
}

################################################################################

answer_1 = {
  "customer_id": "customer_1",
  "client_id": "client_1",
  "channel_ids": "client_1",
  "messages": [
    "Good morning.\nMy name is client_1.\nI need Python developers."
  ],
  "attitude": "arrogant",
  "company_name": "Company of customer 1",
  "features": [
    "feature_1",
    "feature_2"
  ],
  "customer_services": [
    {
      "service_name": "customer 1, service 1",
      "service_desc": "description 1"
    },
    {
      "service_name": "customer 1, service 2",
      "service_desc": "description 2"
    }
  ],
  "reply_ctx": "something"
}
