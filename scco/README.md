# Поднятие проекта

## Работа с микросервисами

- Каждый микросервис содержит в себе `Dockerfile`.
- Сборка и запуск микросервисов осуществляется через `docker-compose`.
- Микросервисы общаются через `RabbitMQ`.
- Для подключения микросервисов к сторонним необходимо поменять переменные окружения в файле `.env` в секции `Set up on server`.
- Для подключения сервисов к существующему `RabbitMQ` нужно указать в файле `.env` в секции `Set up on server` параметры `RMQ_NET` и `RMQ_NET_ALIAS`.
- Для эмулирования работы микросервисов можно подтянуть к себе в корень репозитория папку `outside` из ветки `feature/SCCO-46-outside_rabbitmq`. В папке `outside` есть `README.md`, в котором расположена информация по настройке и запуску. На данный момент `docker-compose.yml` уже настроен для работы с папкой `outside`.
- Для запуска конкретных микросервисов в docker-compose созданы профили (доки смотри в [docker-compose profiles](https://docs.docker.com/compose/profiles/)).
- Чеклист по докеру можно посмотреть в `docs/docker_checklist.md`.

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
   POSTGRES_PORT=5432
   POSTGRES_DB=scco_db
   ```
   Для локального тестирования можно поставить произвольные значения &mdash; всё должно работать.

2) Поднять контейнер с кроликом из папки `outside` (смотри [работу с микросервисами](#работа-с-микросервисами)). **Нужен только RabbitMQ, остальные сервисы поднимать не нужно**.

3) Добавить файлы с ключами в микросервис `ml_generation`. Подробнее смотрите раздел "Файлы с секретами" в [README.md](ml_generation/ml_models/README.md) этого микросервиса.

4) Создать volumes. Из проекта запустить скрипт `setup.sh`:
   ```bash
   ./setup.sh
   ./setup.sh -e # to make external to project volumes (parser bot)
   ./setup.sh -r # recreate volumes
   ```
   Volumes будут созданы в папке `volumes` в корне проекта.

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
   docker-compose stop <service_name>
   docker-compose rm <service_name> # удаляет контейнер сервиса
   docker-compose rmi <service_name> # удаляет образ сервиса
   docker-compose down --rmi all --remove-orphans --volumes # удаляет все контейнеры и образы (даже скачанные)
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

# Note

`POSTGRES_HOST` must be the same as the service name or network alias in `docker compose`!!!!!


# Volumes

Maybe install `local-persist` docker plugin: https://dbafromthecold.com/2018/05/02/changing-the-location-of-docker-named-volumes/

From the `scco` root folder run.
```bash
# Parser bot csv
docker volume create --driver local \
      --name parser_bot_csv_volume \
      --opt type=volume \
      --opt device=$(pwd)/volumes/parser_bot_csv_folder \
      --opt o=bind

# Generated offers
docker volume create --driver local \
      --name parser_bot_csv_volume \
      --opt type=volume \
      --opt device=$(pwd)/volumes/parser_bot_csv_folder \
      --opt o=bind
```

# Start services
Send to `scco_debug_data_preprocessing_queue` message:
```json
{
  "customer_id": "customer_it",
  "parsed_csv": "Messages_Request_From_2024_04_29.csv"
}
```
