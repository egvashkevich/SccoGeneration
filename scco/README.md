# Поднятие проекта

## Работа с микросервисами

- Каждый микросервис содержит в себе `Dockerfile`.
- Сборка и запуск микросервисов осуществляется через `docker-compose`.
- Микросервисы общаются через `RabbitMQ`.
- Для подключения микросервисов к сторонним необходимо поменять переменные окружения в файле `.env` в секции `Set up on server`.
- Для подключения сервисов к существующему `RabbitMQ` нужно указать в файле `.env` в секции `Set up on server` параметры `RMQ_NET` и `RMQ_NET_ALIAS`.
- Для эмулирования работы микросервисов можно подтянуть к себе в корень репозитория папку `outside` из ветки `feature/SCCO-46-outside_rabbitmq`. В папке `outside` есть `README.md`, в котором расположена информация по настройке и запуску. На данный момент `docker-compose.yml` уже настроен для работы с папкой `outside`.
- Для запуска конкретных микросервисов в docker-compose созданы профили (доки смотри в [docker-compose profiles](https://docs.docker.com/compose/profiles/))

## Доступные микросервисы

* `data_preprocessing`
  * Получает `csv` файл с запросами клиентов.
  * Фильтрует собщения.
  * Передаёт информацию сервису `ml_generation`

* `ml_generation`
  * Генерирует текст корпоративного предложения по сообщениям клиентов.
  * Отправляет сгенерированный текст сервису `pdf_generation`

* `pdf_generation`
  * Вставляет текст корпоративного предложения в шаблонный `pdf` документ.
  * Отправляет сгенерированный `pdf` стороннему сервису.

* `db_funstional_service`
  * Хранит данные о заказчиках, клиентах и запросах.
  * Остальные сервисы пользуются этим в качестве базы данных.

* `customer_creator`
  * Вставляет данные заказчиков в базу данных через `db_funstional_service`.

## Запуск и остановка

### Пререквизиты

1) Перед запуском нужно создать файл `scco/db_functional_service/.env.secret.postgres`. Там нужно прописать данные вида:
   ```text
   POSTGRES_USER=scco_postgres
   POSTGRES_PASSWORD=scco_password
   POSTGRES_HOST=scco_postgres_host
   POSTGRES_PORT=5432
   POSTGRES_DB=scco_db
   ```
   Для локального тестирования можно поставить произвольные значения &mdash; всё должно работать.

2) Поднять контейнер с кроликом из папки `outside` (смотри [работу с микросервисами](#работа-с-микросервисами)). **Нужен только RannitMQ, остадльные сервисы поднимать не нужно**.

### Запуск и остановка всех микросервисов

Нужно перейти в папку `scco` и выполнить:
```bash
# Запуск
docker-compose up --build -d
# Остановка
docker-compose down
docker-compose down --remove-orphans # удаляет контейнеры
docker-compose down --remove-orphans --volumes # удаляет volume для postgres
docker-compose down --remove-orphans --volumes --rmi all # удаляет все образы
```

После нескольких запусков у вас может образоваться много "висячих" образов, которые будут занимать память. Для **удаления висячих образов** воспользуйтесь командой:
```bash
docker images -f dangling=true # посмотреть список висячих образов
docker rmi $(docker images -f dangling=true -q)
docker image prune # более короткий вариант
```

Для **удаления контейнеров**:
```bash
# Удаление всех остановленных контейнеров.
docker container prune
# Удаление всех <none> контейнеров.
docker ps -a | grep '<none>' | awk '{ print $1; }' | xargs docker rm
```

### Запуск и остановка конкретных сервисов

Этот раздел нужен в основном для дебага.

1) Запускаем `db_functional_service` для взаимодействия с БД:
   ```bash
   # run
   docker-compose --profile crud up --build -d
   # stop
   docker-compose --profile crud down --remove-orphans
   # Stop + delete postgres volume
   docker-compose --profile crud down --remove-orphans --volumes
   ```

2) Теперь, если мы хотим запустить конкретный микросервис `<service_name>`, то нужно из папки `scco` выполнить:
    ```bash
    # run
    docker-compose up --build -d <service_name>
    # stop
    docker-compose down --rmi all --remove-orphans <service_name> # удаляет собранный образ
    ```

Посмотреть текущее состояние сервисов:
```bash
docker-compose ps -a
```


### Удаление контейнеров и образов, связанных с `scco`, вручную

В папке `outside` выполнить команду
```bash
./clear_docker.sh
```
