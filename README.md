# Система создания КП

В этом репозмтории ведётся разработка проекта "Система создания КП"

### Структура репозитория

В директории `machine_learning` происходит вся работа по разработке и обучению моделей ML.

В директории `scco` находится то, что нужно для работы модуля на сервере, в частности, все микросервисы в отдельных директориях и файл `docker-compose.yaml`.

```
<repository scco>
│
├── machine_learning/
│   ├── data/*
│   ├── <notebook>.ipynb
│   └── .gitignore
│
├── scco/
│   ├── database/*
│   ├── <microservice_1>/
│   │    ├── <microservice_1>.py
│   │    ├── <microservice_1>_api.yaml
│   │    ├── Dockerfile
│   │    └── ...
│   │
│   ├── <microservice_2>/*
│   ├── ...
│   │
│   └── docker-compose.yaml
│
├── .gitignore
└── README.md
```
