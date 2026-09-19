from functools import lru_cache
import re
import time
from deep_translator import GoogleTranslator, MyMemoryTranslator


def is_devanagari(text: str) -> bool:
    """Check if string contains Devanagari (Hindi) script."""
    if not text:
        return False
    return bool(re.search(r"[\u0900-\u097F]", str(text)))


@lru_cache(maxsize=256)
def translate_hindi_to_english(text: str) -> str:
    if not isinstance(text, str) or not text.strip():
        return ""

    # Clean Hindi full stops (Danda)
    cleaned_text = text.replace("।", " . ").strip()
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)

    # 1. Primary: GoogleTranslator
    try:
        translated = GoogleTranslator(source="hi", target="en").translate(cleaned_text)
        if translated and not is_devanagari(translated):
            return translated
    except Exception as e:
        print(f"[TRANSLATOR WARNING] Google Hi->En failed: {e}")

    # 2. Fallback: MyMemoryTranslator (Uses full language names or ISO region codes)
    try:
        translated = MyMemoryTranslator(source="hindi", target="english").translate(cleaned_text)
        if translated and not is_devanagari(translated):
            return translated
    except Exception as e:
        print(f"[TRANSLATOR ERROR] MyMemory Hi->En failed: {e}")

    # 3. Last-resort fallback string
    return text


@lru_cache(maxsize=256)
def translate_english_to_hindi(text: str) -> str:
    if not isinstance(text, str) or not text.strip():
        return ""

    cleaned_text = re.sub(r"\s+", " ", text).strip()

    # 1. Primary: GoogleTranslator
    try:
        translated = GoogleTranslator(source="en", target="hi").translate(cleaned_text)
        if translated:
            return translated
    except Exception as e:
        print(f"[TRANSLATOR WARNING] Google En->Hi failed: {e}")

    # 2. Fallback: MyMemoryTranslator
    try:
        translated = MyMemoryTranslator(source="english", target="hindi").translate(cleaned_text)
        if translated:
            return translated
    except Exception as e:
        print(f"[TRANSLATOR ERROR] MyMemory En->Hi failed: {e}")

    return text