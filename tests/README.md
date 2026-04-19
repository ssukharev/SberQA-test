# Автотесты для AI-агента поддержки

## Структура

```
tests/
├── config.py                # URL, пороги, настройки
├── conftest.py              # Фикстуры (API-сессия, хелпер ask)
├── test_assistant.py        # Тесты (позитивные, негативные, безопасность)
├── generate_test_data.py    # Генератор тестовых данных
├── pytest.ini               # Конфигурация pytest
└── README.md                # Этот файл
```

## Установка

```bash
pip install pytest requests
```

## Запуск

1. Запустить мок-API (из корня проекта):
```bash
uvicorn mock_api:app --port 8000
```

2. В отдельном терминале запустить тесты:
```bash
cd tests
pytest
```

## Переменные окружения

| Переменная | По умолчанию | Описание |
|------------|-------------|----------|
| `ASSISTANT_API_URL` | `http://localhost:8000` | URL тестового стенда |

Пример:
```bash
ASSISTANT_API_URL=http://staging.example.com pytest
```

## Генерация тестовых данных

```bash
python generate_test_data.py
```

Создаёт файл `test_data.json` с 20 вариациями вопросов для проверки стабильности.
