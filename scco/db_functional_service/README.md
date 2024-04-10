- [ ] установка постгреса: https://help.ubuntu.com/community/PostgreSQL
- [ ] сериализация объектов




# Разработка

Используем постгру и `peewee` в качестве ORM.

- Типы, поддерживаемые peewee: http://docs.peewee-orm.com/en/latest/peewee/models.html#field-types-table

# API

Формат взаимодействия с БД

# БД

* Метадата + доки методов: https://docs.sqlalchemy.org/en/20/core/metadata.html#metadata-describing

* Working with metadata: https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#tutorial-working-with-metadata

* Unified tutorial: https://docs.sqlalchemy.org/en/20/tutorial/index.html

* Threading with rabbitmq: https://stackoverflow.com/questions/60308045/calling-more-than-one-functions-as-rabbitmq-message

* aio_pika: https://aio-pika.readthedocs.io/en/latest/rabbitmq-tutorial/6-rpc.html

- [ ] Как будут удаляться данные из БД?

sqlalchemy.types.JSON - для хранения json: https://stackoverflow.com/questions/75379948/what-is-correct-mapped-annotation-for-json-in-sqlalchemy-2-x-version

- [ ] [Entity Relationship Diagram](https://miro.com/app/board/uXjVKZsS6Io=/)

Postgres url:
```text
postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]
```

### Pgadmin

* Нажать `Server` -> `Create`.
* Ввести произвольное название сервера.
* В поле `host` ввести название **контейнера**: `scco_crud_test_postgres_container` (если запуск из tests).
* Остальные поля заполнять из файла `.env.secret.postgres`

Link to python multiline string: https://stackoverflow.com/a/48112903/16704057

### Several postgresql databases

Multiple databases vs multiple schemas: https://stackoverflow.com/questions/28951786/postgresql-multiple-database-vs-multiple-schemas

### Installation and run
```bash
./run.sh --file main_test.py
```

### Development

To run postgresql + pgadmin locally (from tests dir).
```bash
docker-compose up --build -d
docker-compose down --remove-orphans --volumes

```


To run service (from service root).
```bash
./run.sh --reinstall --editable --file main_test.py
./run.sh -r -e -f main_test.py # short version
```

Написать про виртуальное окружение в установке.
