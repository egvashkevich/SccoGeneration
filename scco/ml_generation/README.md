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

## Файлы с секретами
Смотри ридми в папке `ml_modules`.
