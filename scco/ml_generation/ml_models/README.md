### Взаимодействие с GigaChatAPI:
- В файле generate описаны структуры для взаимодействия 
- в main.py вы можете найти пример использования
- Для генерации достаточно заимпортить класс GenerateGateWrapper и применить метод generate\_offer\_text для получения OfferInfo из MlClientInfo
- в configs находятся конфиги для использования модели

Для использования нужно в .env файл закинуть 3 константы:
GIGACHAT\_API\_SCOPE = 'GIGACHAT\_API\_PERS' (если юзать как физ лицо)
GIGACHAT\_API\_CLIENT\_ID = ...
GIGACHAT\_API\_CLIENT\_SECRET = ...
