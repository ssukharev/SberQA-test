"""
Фикстуры pytest для тестирования API ассистента.
"""

import time
import pytest
import requests

from config import ASK_ENDPOINT, DEFAULT_USER_ID


@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    yield session
    session.close()


@pytest.fixture
def ask(api_session):
    def _ask(message: str, user_id: str = DEFAULT_USER_ID):
        start = time.time()
        resp = api_session.post(
            ASK_ENDPOINT,
            json={"user_id": user_id, "message": message},
        )
        latency_ms = int((time.time() - start) * 1000)
        resp.raise_for_status()
        return resp.json(), latency_ms

    return _ask
