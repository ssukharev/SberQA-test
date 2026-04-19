<div align="center">
  <h1>QA Тестирование AI-агента поддержки</h1>
</div>

[![Language](https://img.shields.io/badge/Language-Python_3.13-blue.svg)]()
[![Framework](https://img.shields.io/badge/Framework-FastAPI-009688.svg)]()
[![Tests](https://img.shields.io/badge/Tests-pytest-yellow.svg)]()
[![DB](https://img.shields.io/badge/DB-PostgreSQL-336791.svg)]()

Тестовое задание на позицию Стажер-QA. Включает полный цикл тестирования AI-ассистента поддержки клиентов, работающего на базе LLM + RAG.

---

## Структура проекта

```
.
├── mock_api.py              # Мок-API агента (FastAPI)
├── knowledge_base.py        # База знаний агента (8 тем)
├── seed_data.py             # Генерация тестовых данных для БД
├── logs.db                  # SQLite-база с логами (200 записей)
├── requirements.txt
├── README.md
│
├── stage1_bug_reports.md    # Этап 1 — Баг-репорты
├── stage2_sql.md            # Этап 2 — SQL-запросы
├── stage4_regression.md     # Этап 4 — Регрессионное тестирование
│
└── tests/                   # Этап 3 — Автотесты
    ├── test_assistant.py    # 21 тест (pytest)
    ├── conftest.py          # Фикстуры
    ├── config.py            
    ├── generate_test_data.py
    └── README.md
```

## Быстрый старт

```bash
pip install -r requirements.txt
uvicorn mock_api:app --port 8000    # запуск API
cd tests && pytest                   # запуск тестов (в отдельном терминале)
```

---

## Этапы

### Этап 0. Мок-API агента
Мок-сервер на FastAPI, симулирующий поведение ассистента с базой знаний и намеренно заложенными дефектами для тестирования.

`POST /api/assistant/ask` -> `{ "response", "source", "ticket_id" }`

### Этап 1. [Ручное тестирование и баг-репорты](stage1_bug_reports.md)
Исследовательское тестирование агента. Найдено **6 дефектов**: галлюцинация, неверный интент, потеря контекста, over-refusal, промпт-инъекция, высокая задержка. Каждый оформлен как баг-репорт с шагами воспроизведения и анализом.

### Этап 2. [SQL-запросы и аналитика](stage2_sql.md)
SQL-запросы к таблице логов: топ-10 пользователей по тикетам, поиск запросов с высокой задержкой. Предложения по расширению структуры логирования.

### Этап 3. [Автоматизация тестирования](tests/README.md)
21 автотест на pytest: позитивные, негативные, галлюцинации, промпт-инъекции, latency. Используются фикстуры, `parametrize`, конфиг через переменные окружения.

### Этап 4. [Регрессионное тестирование](stage4_regression.md)
Теоретическая часть: подход к формированию регрессионного набора, автоматизация сравнения версий модели (cosine similarity, exact match), метрики отслеживания галлюцинаций.
