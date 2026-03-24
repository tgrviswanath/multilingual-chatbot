"""
Main chat service: detect language → translate to EN → classify intent
→ get response → translate response back to user language.
"""
from app.core.translator import detect_language, translate_to_english, translate_from_english
from app.core.classifier import predict_intent


def chat(message: str, translate_response: bool = True) -> dict:
    """
    Process a chat message end-to-end.
    Returns detected language, intent, English response, and translated response.
    """
    # 1. Detect language
    lang = detect_language(message)

    # 2. Translate to English if needed
    english_message = translate_to_english(message, lang)

    # 3. Classify intent
    intent_result = predict_intent(english_message)

    # 4. Translate response back to user language
    english_response = intent_result["response"]
    if translate_response and lang != "en":
        final_response = translate_from_english(english_response, lang)
    else:
        final_response = english_response

    return {
        "message": message,
        "detected_language": lang,
        "english_message": english_message,
        "intent": intent_result["intent"],
        "confidence": intent_result["confidence"],
        "response_english": english_response,
        "response": final_response,
    }
