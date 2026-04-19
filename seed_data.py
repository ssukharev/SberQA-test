"""
Скрипт для создания и наполнения таблицы logs тестовыми данными.
"""

import sqlite3
import random
import uuid
from datetime import datetime, timedelta


NUM_RECORDS = 200
USER_IDS = [f"user_{i:03d}" for i in range(1, 21)]

SAMPLE_REQUESTS_KB = [
    ("Как сменить пароль?", "Для смены пароля перейдите в Настройки → Безопасность..."),
    ("Какие есть тарифы?", "Мы предлагаем три тарифа: Базовый, Стандарт и Премиум..."),
    ("Как удалить аккаунт?", "Для удаления аккаунта перейдите в Настройки → Аккаунт..."),
    ("Как оплатить подписку?", "Мы принимаем оплату банковскими картами Visa, Mastercard и МИР..."),
    ("Как вернуть деньги?", "Возврат средств возможен в течение 14 дней..."),
    ("Как отключить уведомления?", "Управление уведомлениями доступно в Настройки → Уведомления..."),
    ("Как подключить интеграцию?", "Документация по API доступна по адресу docs.example.com/api..."),
    ("Как включить 2FA?", "Для включения двухфакторной аутентификации перейдите в Настройки..."),
]

SAMPLE_REQUESTS_TICKET = [
    ("Как открыть офис на Марсе?", "К сожалению, я не нашёл ответа на ваш вопрос..."),
    ("Почему у меня списали деньги дважды?", "Я создал тикет, наш специалист свяжется..."),
    ("Ваше приложение удалило мои файлы", "Я создал тикет, наш специалист свяжется..."),
    ("Хочу интеграцию с SAP", "К сожалению, я не нашёл ответа на ваш вопрос..."),
    ("Мой менеджер не отвечает уже неделю", "Я создал тикет, наш специалист свяжется..."),
]


def generate_records():
    records = []
    base_time = datetime.now() - timedelta(days=30)

    heavy_ticket_users = set(USER_IDS[:5])

    for i in range(NUM_RECORDS):
        user_id = random.choice(USER_IDS)
        created_at = base_time + timedelta(
            minutes=random.randint(0, 43200)
        )

        if user_id in heavy_ticket_users:
            use_ticket = random.random() < 0.7
        else:
            use_ticket = random.random() < 0.2

        if use_ticket:
            req_text, resp_text = random.choice(SAMPLE_REQUESTS_TICKET)
            source = "ticket_created"
        else:
            req_text, resp_text = random.choice(SAMPLE_REQUESTS_KB)
            source = "knowledge_base"

        if source == "knowledge_base" and random.random() < 0.08:
            latency_ms = random.randint(5100, 9500)
        else:
            latency_ms = random.randint(150, 2000)

        records.append((
            user_id,
            req_text,
            resp_text,
            source,
            latency_ms,
            created_at.strftime("%Y-%m-%d %H:%M:%S"),
        ))

    return records


def seed_database(db_path: str = "logs.db"):
    conn = sqlite3.connect(db_path)

    conn.execute("DROP TABLE IF EXISTS logs")
    conn.execute("""
        CREATE TABLE logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id VARCHAR NOT NULL,
            request_text TEXT NOT NULL,
            response_text TEXT NOT NULL,
            source VARCHAR NOT NULL,
            latency_ms INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    records = generate_records()
    conn.executemany(
        "INSERT INTO logs (user_id, request_text, response_text, source, latency_ms, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        records,
    )
    conn.commit()


    count = conn.execute("SELECT COUNT(*) FROM logs").fetchone()[0]
    ticket_count = conn.execute(
        "SELECT COUNT(*) FROM logs WHERE source = 'ticket_created'"
    ).fetchone()[0]
    high_latency = conn.execute(
        "SELECT COUNT(*) FROM logs WHERE latency_ms > 5000 AND source = 'knowledge_base'"
    ).fetchone()[0]

    print(f"База данных создана: {db_path}")
    print(f"  Всего записей:          {count}")
    print(f"  Тикетов:                {ticket_count}")
    print(f"  Высокая задержка (KB):  {high_latency}")

    conn.close()



POSTGRES_SCHEMA = """
-- Схема для PostgreSQL (из ТЗ)
CREATE TABLE IF NOT EXISTS logs (
    id          SERIAL PRIMARY KEY,
    user_id     VARCHAR NOT NULL,
    request_text TEXT NOT NULL,
    response_text TEXT NOT NULL,
    source      VARCHAR NOT NULL CHECK (source IN ('knowledge_base', 'ticket_created')),
    latency_ms  INTEGER NOT NULL,
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_logs_user_id ON logs (user_id);
CREATE INDEX idx_logs_source ON logs (source);
CREATE INDEX idx_logs_latency ON logs (latency_ms);
CREATE INDEX idx_logs_created_at ON logs (created_at);
"""


if __name__ == "__main__":
    seed_database()
    print(f"\nPostgreSQL-схема (справочно):\n{POSTGRES_SCHEMA}")
