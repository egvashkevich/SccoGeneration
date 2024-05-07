# import ml_models.gigachat_api_gate.api as ml_models_api
import ml_models.co_gen.api as co_gen_api
import ml_models.white_list_generation.api as whitelist_gen_api

# TODO: expected API as below

co_gen = co_gen_api.SCCOGenerator()

request = {
    "customer_id": "customer_1",
    "contact_info": "<@telegram_link>",
    "company_name": "Web сфера",
    'channel_ids': "Outstaffing",
    'messages': ['всем привет. мы - команда smartbrainio и сейчас мы в поиске java senior developer мы в поиске кандидата на длительный проект который готов присоединиться в нашу команду требования java8java11 опыт не менее 7 лет уровень английского языка от в1. spring spring-boot spring-data spring-security spring-web spring-aop. опыт проектирования и реализации микросервисов. junit. jsjsp. опыт работы с реляционными бд sqlserver postgres mysql. большим плюсом будет опыт работы с dockerkubernetes aws. желателен опыт работа с gitjenkins elk vaadin. плюсом будет опыт работы с hibernate axis struts vaadin jooq hk2. опыт проектирования production систем с нуля. гибкое мышление disagree and commit principle задачи проектирование и реализация отказоустойчивых масштабируемых и высоконагруженных приложений. проектирование и разработка интерфейсов микро сервисов сервисов soaprest библиотек. проектирование процессов по бесшовной миграции текущих приложений на новые анализ и рефакторинг текущих приложений как часть этого процесса. разработка unit тестов. написание sql запросовхранимых процедурфункций проектирование схем бд оптимизация запросов. использование и развитие инструментов командной работы git ci. сопровождение текущего функционала библиотеки soaprest сервисы вэб-приложения в основном с целью изучения существующего функционала. проведение code review. наставничество telegram @lera_smartbrainio'],
    "black_list": [
        "php",
        "wordpress",
        "c#",
    ],
    "tags": [
        "frontend",

        "android",
        "ios",

        "react",
        "nodejs",

        "javascript",
        "vue",

        "typescript",

        "figma",
        "flutter",
        "photoshop",
        "web",

        "css",
        "css3",
        "html",
        "html5",

        "REST",
        "вёрстка",
        "веб-сайт"
    ],
    "white_list": [
        "frontend",

        "android",
        "ios",

        "react",
        "nodejs",

        "javascript",
        "vue",

        "typescript",

        "figma",
        "flutter",
        "photoshop",
        "web",

        "css",
        "css3",
        "html",
        "html5",

        "REST",
        "вёрстка",
        "веб-сайт"
    ],
    "specific_features": [
        "Мы - российская компания по разработке программного обеспечения, ориентированная на технологические процессы.",
        "Мы помогаем другим компаниям взаимодействовать со своей аудиторией с помощью высококачественных веб-приложений и мобильных устройств на платформе android.",
        "У нас имеется 25-летний опыт веб-разработки и веб-хостинга",
        "Мы рассматриваем наших клиентов как стратегических деловых партнеров. Поэтому выбор нас для создания вашего веб-сайта - это только первый этап в долгосрочных деловых отношениях.",
        "У нас сотни клиентов по всему миру. Некоторые из них работают у нас более 15 лет, что является беспрецедентным в этой отрасли."
    ],
    "customer_services": [
        {
            "customer_id": "customer_1",
            "service_name": "Создание MVP",
            "service_desc": "Запускаете новый продукт? Наши услуги по разработке MVP основаны на быстром прототипировании и гибкой методологии, позволяющей быстро и эффективно выводить ваши идеи на рынок."
        },
        {
            "customer_id": "customer_1",
            "service_name": "UX/UI дизайн",
            "service_desc": "Наши услуги по дизайну продуктов позволяют по-новому взглянуть на разработку программного обеспечения, которую возглавляют эксперты в области консалтинга по дизайну продуктов. Мы не просто консультанты по дизайну продуктов; мы новаторы в разработке дизайна, ориентированного на пользователя."
        },
        {
            "customer_id": "customer_1",
            "service_name": "Модернизация устаревшего UI",
            "service_desc": "Преобразуем ваш пользовательский интерфейс в соответствии с современными стандартами. Наши услуги по модернизации пользовательского интерфейса делают ваши приложения более привлекательными и удобными для пользователя."
        },
    ]
}


main_response = co_gen.generate(request)

print(main_response["main_text"])

#import json
#for num in range(3, 15+1):
#    with open('clients_messages/'+f'clients_messages_{num}.txt', 'r', encoding='utf-8') as f:
#        d = json.load(f)
#        request['messages'] = d['messages']
#    print(request['messages'])
#    main_response = co_gen.generate(request)
#    with open(f'answers/ans{num}.txt', 'w') as f:
#        f.write(main_response['main_text'])

