import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


# Download required NLTK resources



# Initialize tools
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def preprocess_english(text):
    """
    Preprocess an English complaint.

    Steps:
    1. Convert text to lowercase
    2. Remove unnecessary characters
    3. Tokenize
    4. Remove stopwords
    5. Lemmatize words
    6. Return cleaned text
    """

    # Make sure input is a string
    if not isinstance(text, str):
        return ""

    # 1. Convert to lowercase
    text = text.lower()

    # 2. Keep only letters and spaces
    text = re.sub(r"[^a-z\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    # 3. Tokenization
    tokens = word_tokenize(text)

    # 4. Remove stopwords
    tokens = [
        word for word in tokens
        if word not in stop_words
    ]

    # 5. Lemmatization
    tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
    ]

    # 6. Convert tokens back to text
    cleaned_text = " ".join(tokens)

    return cleaned_text