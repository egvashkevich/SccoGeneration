# Поднятие кролика локально для тестирования

## Доступные сервисы
* `client_queries` - сервис, который отвечает за бота, от которого мы получаем `csv` файл с информацией.
* `generated_offers` - сервис, которому мы отправляем сгенерированный pdf файл.
* `rabbitmq` - брокер

## Запуск и остановка

### Запуск и остановка `RabbitMQ`

Нужно перейти в папку `rabbitmq` и выполнить:
```bash
# run
docker-compose --env-file ../.env up --build -d
# stop
docker-compose --env-file ../.env down --remove-orphans --volumes
```
По идее достаточно запустить его перед началом работы и выключить в конце разработки и забыть. Но если по непонятным причинам выскакивает ошибка `Unexpected error: [Errno -3] Temporary failure in name resolution`, то перезапуск контейнера с `RabbitMQ` помогает 

### Запуск и остановка сторонних сервисов
Из папки `outside` нужно выполнить:
```bash
# start
docker-compose up --build -d
# stop
docker-compose down --remove-orphans --volumes
```

Запуск отдельных сервисов. Из папки `outside` нужно выполнить:
```bash
# start
docker-compose --profile queries up -d
docker-compose --profile offers up -d
# stop
docker-compose --profile queries down --rmi all --remove-orphans
docker-compose --profile offers down --rmi all --remove-orphans
```

Посмотреть текущее состояние сервисов:
```bash
docker-compose ps -a
```


### Удаление контейнеров и образов связанных с `scco` вручную
```bash
./clear_docker.sh
```
