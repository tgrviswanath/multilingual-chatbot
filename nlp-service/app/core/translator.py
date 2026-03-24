"""
Language detection using langdetect.
Translation to English using Helsinki-NLP MarianMT models.
Supports: French, Spanish, Italian, Portuguese, Romanian (ROMANCE group)
and German, Dutch via separate models.
"""
from langdetect import detect, LangDetectException

# Map language code → Helsinki-NLP MarianMT model
TRANSLATION_MODELS = {
    "fr": "Helsinki-NLP/opus-mt-fr-en",
    "es": "Helsinki-NLP/opus-mt-es-en",
    "de": "Helsinki-NLP/opus-mt-de-en",
    "it": "Helsinki-NLP/opus-mt-it-en",
    "pt": "Helsinki-NLP/opus-mt-ROMANCE-en",
    "nl": "Helsinki-NLP/opus-mt-nl-en",
    "ru": "Helsinki-NLP/opus-mt-ru-en",
    "zh-cn": "Helsinki-NLP/opus-mt-zh-en",
    "ar": "Helsinki-NLP/opus-mt-ar-en",
}

# Lazy-loaded translation pipelines cache
_translators: dict = {}


def detect_language(text: str) -> str:
    try:
        return detect(text)
    except LangDetectException:
        return "en"


def translate_to_english(text: str, src_lang: str) -> str:
    """Translate text to English. Returns original text if lang is English or unsupported."""
    if src_lang == "en" or src_lang not in TRANSLATION_MODELS:
        return text

    model_name = TRANSLATION_MODELS[src_lang]
    if model_name not in _translators:
        from transformers import pipeline as hf_pipeline
        _translators[model_name] = hf_pipeline(
            "translation",
            model=model_name,
            device=-1,
        )

    result = _translators[model_name](text, max_length=512)
    return result[0]["translation_text"]


def translate_from_english(text: str, tgt_lang: str) -> str:
    """Translate English response back to target language."""
    if tgt_lang == "en":
        return text

    # Reverse model map: en → target
    reverse_models = {
        "fr": "Helsinki-NLP/opus-mt-en-fr",
        "es": "Helsinki-NLP/opus-mt-en-es",
        "de": "Helsinki-NLP/opus-mt-en-de",
        "it": "Helsinki-NLP/opus-mt-en-it",
        "pt": "Helsinki-NLP/opus-mt-en-ROMANCE",
        "nl": "Helsinki-NLP/opus-mt-en-nl",
        "ru": "Helsinki-NLP/opus-mt-en-ru",
        "zh-cn": "Helsinki-NLP/opus-mt-en-zh",
        "ar": "Helsinki-NLP/opus-mt-en-ar",
    }

    if tgt_lang not in reverse_models:
        return text

    model_name = reverse_models[tgt_lang]
    if model_name not in _translators:
        from transformers import pipeline as hf_pipeline
        _translators[model_name] = hf_pipeline(
            "translation",
            model=model_name,
            device=-1,
        )

    result = _translators[model_name](text, max_length=512)
    return result[0]["translation_text"]
