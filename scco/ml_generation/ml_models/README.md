## Файлы с секретами
1) Файл `api_token.secret.env` по пути `scco/ml_generation/ml_models/src/ml_models/co_gen/api_token.secret.env`
   Содержимое файла:
   ```bash
   GIGACHAT_API_SCOPE="GIGACHAT_API_PERS"
   GIGACHAT_API_CLIENT_ID=<see_below>
   GIGACHAT_API_CLIENT_SECRET=<see_below>
   ```
   Для получения значений `GIGACHAT_API_CLIENT_ID` и `GIGACHAT_API_CLIENT_SECRET` нужно:
   1) Перейти на сайт [developers.sber.ru](https://developers.sber.ru/docs/ru/gigachat/individuals-quickstart)
   2) В правой части экрана нажать `подключить сервис` -> `начать пользоваться как физлицо`
   3) Зайти в аккаунт (например, по номеру телефона)
   4) В правой части экрана скопировать `Client ID` и вставить в переменную `GIGACHAT_API_CLIENT_ID`
   5) Нажать `Generate new` -> `Generate new one anyway`.
   6) Скопировать значение `Client Secret` в переменную `GIGACHAT_API_CLIENT_SECRET`
   **Note** Для юридических лиц инструкция немного другая, подробнее узнавайте на сайте.

<!-------------------------------------------------------------------->

### Использование
* Все модели располагаются в пакете `ml_models`.
* Настройка конфигов: TODO
