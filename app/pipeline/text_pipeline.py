from app.preprocessing.english_preprocessing import preprocess_english
from app.preprocessing.hindi_preprocessing import preprocess_hindi
from app.translation.translator import translate_hindi_to_english


def process_complaint(text, language):
    """
    Process a complaint based on the selected language.

    English:
        Complaint → English preprocessing

    Hindi:
        Complaint → Hindi preprocessing
                  → English translation
                  → English preprocessing

    Returns:
        original_text
        hindi_processed
        translated_text
        english_processed
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

        translated_text = translate_hindi_to_english(
    hindi_processed
)

        english_processed = preprocess_english(
            translated_text
        )

        return {
            "original_text": text,
            "hindi_processed": hindi_processed,
            "translated_text": translated_text,
            "english_processed": english_processed
        }

    else:
        raise ValueError(
            "Language must be either 'Hindi' or 'English'."
        )