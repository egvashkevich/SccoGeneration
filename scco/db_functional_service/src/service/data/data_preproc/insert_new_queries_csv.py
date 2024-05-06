request_simple = {
    "request_name": "insert_new_queries_csv",
    "reply": {
        "exchange": "scco_test_exchange",
        "routing_key": "scco_test_rk",
    },
    "reply_ctx": "something",  # not required
    "request_data": {
        "csv_path": "path/to/inserted.csv",
    }
}

################################################################################

answer_simple = {
  "csv_path": "path/to/inserted.csv",
  "reply_ctx": "something"
}
