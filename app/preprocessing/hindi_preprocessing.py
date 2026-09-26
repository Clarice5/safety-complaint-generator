import re
import unicodedata


def preprocess_hindi(text):
    """
    Perform light preprocessing on Hindi complaint text.

    Hindi text is only lightly cleaned because it will
    be translated into English later.

    Steps:
    1. Normalize Unicode
    2. Remove unnecessary punctuation/symbols
    3. Normalize whitespace
    4. Return cleaned Hindi text
    """

    # Make sure input is a string
    if not isinstance(text, str):
        return ""

    # 1. Unicode normalization
    text = unicodedata.normalize("NFC", text)

    # 2. Remove unnecessary punctuation and symbols
    # Keep Hindi characters, English characters, numbers and spaces
    text = re.sub(
        r"[^\u0900-\u097F a-zA-Z0-9]",
        " ",
        text
    )

    # 3. Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text