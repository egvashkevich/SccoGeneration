import os


def from_env(var_name):
    if var_name in os.environ:
        return os.environ[var_name]
    print(f"Warning: environment variable {var_name} not found, setting to None")
    return None


RABBIT_ADDRESS = from_env('RMQ_NET_ALIAS')

if RABBIT_ADDRESS is not None:
    IN_EXCHANGE = from_env('DATA_PREPROCESSING_EXCHANGE')
    IN_QUEUE = from_env('DATA_PREPROCESSING_QUEUE')
    IN_ROUTING_KEY = from_env('DATA_PREPROCESSING_ROUTING_KEY')

    DB_FUNCTIONAL_SERVICE_EXCHANGE = from_env('DB_FUNCTIONAL_SERVICE_EXCHANGE')
    DB_FUNCTIONAL_SERVICE_QUEUE = from_env('DB_FUNCTIONAL_SERVICE_QUEUE')
    DB_FUNCTIONAL_SERVICE_ROUTING_KEY = from_env('DB_FUNCTIONAL_SERVICE_ROUTING_KEY')

    OUT_EXCHANGE = from_env('ML_GENERATION_EXCHANGE')
    OUT_QUEUE = from_env('ML_GENERATION_QUEUE')
    OUT_ROUTING_KEY = from_env('ML_GENERATION_ROUTING_KEY')

    CONTAINS_QUERY_EXCHANGE = IN_EXCHANGE  # IN_EXCHANGE + '_contains'
    CONTAINS_QUERY_QUEUE = IN_QUEUE + '_contains'
    CONTAINS_QUERY_ROUTING_KEY = IN_ROUTING_KEY + '_contains'

    NEW_QUERIES_CSV_FOLDER = 'new_queries/'
    NEW_QUERIES_PREFIX_FOR_SENDING = '../data_preprocessing/new_queries/'

    # TODO
    INSERT_BEFORE_PREPROCESSING_QUERY_EXCHANGE = 'insert_before_preprocessing'
    INSERT_BEFORE_PREPROCESSING_QUERY_QUEUE = 'insert_before_preprocessing_queue'
    INSERT_BEFORE_PREPROCESSING_QUERY_ROUTING_KEY = 'insert_before_preprocessing_rk'

    # CUSTOMER_LISTS_QUERY_EXCHANGE = 'customer_lists'
    # CUSTOMER_LISTS_QUERY_QUEUE = 'customer_lists_queue'
    # CUSTOMER_LISTS_QUERY_ROUTING_KEY = 'customer_lists_rk'

    # INSERT_AFTER_PREPROCESSING_QUERY_EXCHANGE = 'insert_after_preprocessing'
    # INSERT_AFTER_PREPROCESSING_QUERY_QUEUE = 'insert_after_preprocessing_queue'
    # INSERT_AFTER_PREPROCESSING_QUERY_ROUTING_KEY = 'insert_after_preprocessing_rk'
