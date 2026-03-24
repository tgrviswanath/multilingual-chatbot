import pytest
from unittest.mock import patch, MagicMock
from app.core.intents import INTENTS
from app.core.translator import detect_language


def test_intents_have_required_keys():
    for intent, data in INTENTS.items():
        assert "examples" in data
        assert "response" in data
        assert isinstance(data["response"], str)


def test_unknown_intent_exists():
    assert "unknown" in INTENTS


def test_detect_english():
    lang = detect_language("Hello, how are you today?")
    assert lang == "en"


def test_detect_french():
    lang = detect_language("Bonjour, comment allez-vous?")
    assert lang == "fr"


def test_detect_empty_returns_en():
    lang = detect_language("")
    assert lang == "en"


@patch("app.core.classifier.joblib.load")
def test_predict_intent(mock_load):
    from app.core.classifier import train_and_save
    # Train a real model in-memory for testing
    train_and_save()

    from app.core.classifier import predict_intent
    result = predict_intent("hello")
    assert result["intent"] in INTENTS
    assert "response" in result
    assert 0 <= result["confidence"] <= 1
