from deep_translator import GoogleTranslator
import time


def translate_hindi_to_english(text):
    """
    Translate Hindi text into English.
    """

    if not isinstance(text, str) or not text.strip():
        return ""

    text = text.replace("।", "").strip()

    for attempt in range(3):
        try:
            translated_text = GoogleTranslator(
                source="hi",
                target="en"
            ).translate(text)

            if translated_text:
                return translated_text

        except Exception as e:
            print(
                f"Hindi → English attempt {attempt + 1} failed: {e}"
            )
            time.sleep(2)

    return ""


def translate_english_to_hindi(text):
    """
    Translate English text into Hindi.
    """

    if not isinstance(text, str) or not text.strip():
        return ""

    for attempt in range(3):
        try:
            translated_text = GoogleTranslator(
                source="en",
                target="hi"
            ).translate(text)

            if translated_text:
                return translated_text

        except Exception as e:
            print(
                f"English → Hindi attempt {attempt + 1} failed: {e}"
            )
            time.sleep(2)

    return ""