import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

MOCK_RESULT = {
    "message": "Hello",
    "detected_language": "en",
    "english_message": "Hello",
    "intent": "greeting",
    "confidence": 0.9,
    "response_english": "Hello! How can I help you today?",
    "response": "Hello! How can I help you today?",
}


@patch("app.core.service.chat", new_callable=AsyncMock)
def test_chat_endpoint(mock_chat):
    mock_chat.return_value = MOCK_RESULT
    response = client.post("/api/v1/chat", json={"message": "Hello"})
    assert response.status_code == 200
    assert response.json()["intent"] == "greeting"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
