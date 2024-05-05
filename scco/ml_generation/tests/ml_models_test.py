# import ml_models.gigachat_api_gate.api as ml_models_api
import ml_models.co_gen.api as co_gen_api

# TODO: expected API as below

model = co_gen_api.SCCOGenerator('co_gen/configs')

request = {
    "customer_id": "customer_1",
    "client_id": "client_1",
    "channel_ids": [
        "phystech.career"
    ],
    "messages": [
        "Добрый день, мне нужег опытный python-разработчик. Мне нужно разработать бота на питоне"
    ],
    "attitude": "arrogant",
    "company_name": "Owl-web",
    "black_list": [
        "fuck",
        "shit",
        "nigger"
    ],
    "tags": [
        "python",
        "b2b"
    ],
    "white_list": [
        "python_synonym",
        "b2b_synonym"
    ],
    "specific_features": [
        "10-летний опыт, много довольных клиентов"
    ],
    "customer_services": [
        {
            "service_name": "Python-бот",
            "service_desc": "Делаем tg-ботов под любые нужды"
        },
        {
            "service_name": "flask/django",
            "service_desc": "Разработка бэка на питоне"
        }
    ],
    "reply_ctx": "something"
}

answer = model.generate_offer_text(request)

print(answer["main_text"])
