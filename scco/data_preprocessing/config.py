RABBIT_ADDRESS = 'localhost'

IN_QUEUE = 'in_queue'
OUT_QUEUE = 'from_preprocessing_to_ml'

CONTAINS_QUERY_EXCHANGE = 'contains_query'
CONTAINS_QUERY_ROUTING_KEY = ''  # TODO

NEW_QUERIES_CSV_FOLDER = 'new_queries/'
NEW_QUERIES_PREFIX_FOR_SENDING = '../data_preprocessing/new_queries/'

BLACK_LIST_QUERY_EXCHANGE = 'black_list'
BLACK_LIST_QUERY_ROUTING_KEY = ''

INSERT_AFTER_PREPROCESSING_QUERY_EXCHANGE = 'insert_after_preprocessing'
INSERT_AFTER_PREPROCESSING_QUERY_ROUTING_KEY = ''
