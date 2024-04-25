def add_reply_ctx(srv_query_data, answer):
    if "reply_ctx" in srv_query_data:
        answer["reply_ctx"] = srv_query_data["reply_ctx"]
