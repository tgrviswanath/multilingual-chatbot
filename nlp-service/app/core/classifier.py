"""
Intent classifier using TF-IDF + LinearSVC.
Trained on the FAQ intent examples from intents.py.
Falls back to 'unknown' intent if confidence is low.
"""
import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from app.core.intents import INTENTS

_MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")
_pipeline = None
_encoder = None


def _load():
    global _pipeline, _encoder
    if _pipeline is None:
        _pipeline = joblib.load(os.path.join(_MODEL_DIR, "intent_pipeline.pkl"))
        _encoder = joblib.load(os.path.join(_MODEL_DIR, "label_encoder.pkl"))


def train_and_save():
    """Train intent classifier and save to models/."""
    os.makedirs(_MODEL_DIR, exist_ok=True)
    texts, labels = [], []
    for intent, data in INTENTS.items():
        for example in data["examples"]:
            texts.append(example)
            labels.append(intent)

    encoder = LabelEncoder()
    y = encoder.fit_transform(labels)

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=3000)),
        ("clf", LinearSVC(max_iter=1000, C=1.0)),
    ])
    pipeline.fit(texts, y)

    joblib.dump(pipeline, os.path.join(_MODEL_DIR, "intent_pipeline.pkl"))
    joblib.dump(encoder, os.path.join(_MODEL_DIR, "label_encoder.pkl"))
    print(f"Intent model saved to {_MODEL_DIR}")


def predict_intent(text: str) -> dict:
    _load()
    label_id = _pipeline.predict([text])[0]
    intent = _encoder.inverse_transform([label_id])[0]

    # Decision function scores for confidence estimate
    scores = _pipeline.decision_function([text])[0]
    max_score = float(scores.max())
    # Normalize to rough confidence: low score → unknown
    confidence = round(min(max(max_score / 3.0, 0.0), 1.0), 3)

    if confidence < 0.2:
        intent = "unknown"

    return {
        "intent": intent,
        "confidence": confidence,
        "response": INTENTS.get(intent, INTENTS["unknown"])["response"],
    }
