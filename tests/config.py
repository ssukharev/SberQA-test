"""
Конфигурация тестового окружения.
URL и пороговые значения вынесены сюда, чтобы не хардкодить в тестах.
"""

import os

BASE_URL = os.getenv("ASSISTANT_API_URL", "http://localhost:8000")
ASK_ENDPOINT = f"{BASE_URL}/api/assistant/ask"

MAX_LATENCY_MS = 3000

DEFAULT_USER_ID = "test_user"
