# Этап 2. Работа с данными и SQL

## Задача 1

Напишите SQL-запрос, который выводит топ-10 пользователей, у которых чаще всего ответы приходили из источника ticket_created (т.е. агент не мог ответить и создавал тикет).


```sql
SELECT 
    user_id,
    COUNT(*) FILTER (WHERE source = 'ticket_created') AS ticket_count
    , COUNT(*) AS total_requests
    , ROUND(
        100.0 * COUNT(*) FILTER (WHERE source = 'ticket_created') / COUNT(*),
        1
    ) AS ticket_pct
FROM logs
GROUP BY user_id
ORDER BY ticket_count DESC
LIMIT 10;
```


## Задача 2

Напишите SQL-запрос для поиска сессий, где агент отвечал с высокой задержкой (> 5 секунд) и при этом ответ был из knowledge_base. Отсортируйте по убыванию задержки.

```sql
SELECT 
    id
    , user_id
    , request_text
    , response_text
    , latency_ms
    , created_at
FROM logs
WHERE latency_ms > 5000
  AND source = 'knowledge_base'
ORDER BY latency_ms DESC;
```


## Задача 3 (опциональная)

### Текущие ограничения

Текущая таблица `logs` фиксирует факт запроса и ответа, но не даёт информации
о *качестве* ответа. Невозможно определить: была ли галлюцинация, насколько
модель была уверена в ответе, какие фрагменты из базы знаний использовались.

### Предлагаемые новые поля

```sql
ALTER TABLE logs ADD COLUMN confidence_score  FLOAT;
ALTER TABLE logs ADD COLUMN retrieved_chunks  JSONB;
ALTER TABLE logs ADD COLUMN retrieval_score   FLOAT;
ALTER TABLE logs ADD COLUMN model_version     VARCHAR(50);
ALTER TABLE logs ADD COLUMN intent            VARCHAR(100);
ALTER TABLE logs ADD COLUMN session_id        VARCHAR(100);
ALTER TABLE logs ADD COLUMN safety_flags      JSONB;
ALTER TABLE logs ADD COLUMN feedback          VARCHAR(20);
```

### Описание полей

| Поле | Тип | Зачем нужно |
|------|-----|-------------|
| `confidence_score` | FLOAT | Уверенность модели в ответе (0.0–1.0). Низкий score - возможная галлюцинация. |
| `retrieved_chunks` | JSONB | Какие фрагменты из KB использовались. Пусто + ответ дан = галлюцинация. |
| `retrieval_score` | FLOAT | Лучший score среди найденных чанков. Низкий - нет релевантных данных в KB. |
| `model_version` | VARCHAR | Версия модели/промпта. Нужно для регрессионного тестирования. |
| `intent` | VARCHAR | Определённый интент (`password_reset`, `unknown` и т.д.). Для анализа ошибок маршрутизации. |
| `session_id` | VARCHAR | ID сессии диалога. Для группировки сообщений и анализа потери контекста. |
| `safety_flags` | JSONB | Какие фильтры безопасности сработали. Для настройки баланса safety/полезность. |
| `feedback` | VARCHAR | Оценка пользователя (`positive`/`negative`). Для поиска проблемных ответов. |
