# import ml_models.gigachat_api_gate.api as ml_models_api
import ml_models.co_gen.api as co_gen_api
import ml_models.white_list_generation.api as whitelist_gen_api

# TODO: expected API as below

co_gen = co_gen_api.SCCOGenerator()
whitelist_gen = whitelist_gen_api.KeyWordsGenerator()

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

whitelist = whitelist_gen.generate(request)
main_response = co_gen.generate(request)

print(main_response["main_text"])
print(whitelist)
