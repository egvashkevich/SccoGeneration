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
  * Отбирает те сообщения (запросы), в которых нет запрещённых слов.
  * Передаёт информацию сервису `ml_generation`

* `ml_generation`
  * Генерирует текст корпоративного предложения по корпоративному предложению
  * Отправляет сгенерированный текст сервису `pdf_generation`

* `pdf_generation`
  * Вставляет текст корпоративного предложения в шаблонный `pdf` документ.
  * Отправляет сгенерированный `pdf` стороннему сервису.

* `db_crud_execution`
  * Хранит данные о клиентах, запросах, а также логи микросервисов.


## Запуск и остановка

Перед запуском нужно создать файл `scco/db_crud_execution/.env.secret.postgres`. Там нужно прописать данные вида:
```text
POSTGRES_USER=scco_postgres
POSTGRES_PASSWORD=scco_password
POSTGRES_HOST=scco_postgres_host
POSTGRES_PORT=5432
POSTGRES_DB=scco_db
```
Для локального тестирования можете поставить произвольные значения &mdash; всё должно работать.

Предполагается, что у вас подняты микросервисы из папки `outside` (смотри [работу с микросервисами](#работа-с-микросервисами)).

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

Если в файле `.env` не определена переменная `COMPOSE_PROFILES`, то профиль придётся указывать вручную:
```bash
# Запуск
docker-compose --profile all up --build -d
# Остановка
docker-compose --profile all down
# Остановка с удалением всех образов
docker-compose --profile all down --rmi all --remove-orphans
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

1) Запускаем postgres (можно **пропустить шаг**, если вы не разрабатываете `db_crud_execution` микросервис):
    ```bash
    # run
    docker-compose --profile postgres up -d
    # stop
    docker-compose --profile postgres down --remove-orphans --volumes # не удаляет образы
    ```

2) Запускаем `db_crud_execution` для взаимодействия с БД:
   ```bash
   # run
   docker-compose --profile crud up --build -d
   # stop
   docker-compose --profile crud down --remove-orphans
   # Stop + delete postgres volume
   docker-compose --profile crud down --remove-orphans --volumes
   ```

3) Теперь, если мы хотим запустить конкретный микросервис `<service_name>`, то нужно из папки `scco` выполнить:
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
