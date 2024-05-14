customer_creator/
├── Dockerfile
├── pyproject.toml
├── requirements.txt
├── .env
├── src/
│   ├── broker_for_creator/
│   │   ├── Broker.py
│   │   ├── RmqBroker.py
│   ├── customer_creator/
│   │   ├── main.py
│   │   |
│   │   └── steps/
│   │       └── insertToDb.py
│   ├── utils/
│   │   ├── app_config.py
│   │   └── parse_env.py
