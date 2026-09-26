import re
from app.preprocessing.english_preprocessing import preprocess_english
from app.preprocessing.hindi_preprocessing import preprocess_hindi
from app.translation.translator import translate_hindi_to_english


def is_devanagari(text: str) -> bool:
    """Check if string contains Devanagari (Hindi) script."""
    if not text:
        return False
    return bool(re.search(r"[\u0900-\u097F]", str(text)))


def process_complaint(text, language):
    """
    Process a complaint based on the selected language.
    """
    if not isinstance(text, str) or not text.strip():
        return {
            "original_text": "",
            "hindi_processed": "",
            "translated_text": "",
            "english_processed": ""
        }

    language = language.lower()

    # English complaint
    if language == "english":
        english_processed = preprocess_english(text)
        return {
            "original_text": text,
            "hindi_processed": "",
            "translated_text": text,
            "english_processed": english_processed
        }

    # Hindi complaint
    elif language == "hindi":
        hindi_processed = preprocess_hindi(text)

        # 1. Translate original raw text (text), NOT preprocessed text (hindi_processed)
        translated_text = translate_hindi_to_english(text)

        # Safety fallback if translation returns empty or raw Hindi
        if not translated_text or is_devanagari(translated_text):
            translated_text = translate_hindi_to_english(hindi_processed) or text

        # 2. Preprocess English translated text for classification
        english_processed = preprocess_english(translated_text)

        return {
            "original_text": text,
            "hindi_processed": hindi_processed,
            "translated_text": translated_text,
            "english_processed": english_processed
        }

    else:
        raise ValueError("Language must be either 'Hindi' or 'English'.")