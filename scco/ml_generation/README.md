# ML generation

## Структура

## Тестирование

* Очень хорошая документация по `pytest`: https://habr.com/ru/articles/426699/

## CI
Нужно из папки микросервиса `ml_generation` выполнить:
```bash
docker build -t scco_test_ml_generation .
docker run --name scco_test_ml_generation scco_test_ml_generation pytest
```

## Как запускать локально:

Из данной дирректори (scco/ml_generation) выполните
```
pip install ./ml_models
pip install .
```
После этого пример использования можно найти в 
```
scco/scco/ml_generation/src/ml_generation/main_test.py  
```
Достаточно запустить через 
```
python3 main_test.py
```
