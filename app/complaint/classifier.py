import os
import re
import string
import joblib
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np

# Project root directory
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

MODEL_DIR = os.path.join(BASE_DIR, "models")

# Load Anaya's trained model and TF-IDF vectorizer
vectorizer = joblib.load(
    os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
)

model = joblib.load(
    os.path.join(MODEL_DIR, "complaint_model.pkl")
)


stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def preprocess_for_model(text):
    """
    Preprocessing used by Anaya's trained model.
    """

    if not isinstance(text, str):
        return ""

    text = text.lower()

    text = re.sub(
        r"http\S+|www\S+|https\S+",
        "",
        text
    )

    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    text = re.sub(r"\d+", "", text)

    text = re.sub(r"\s+", " ", text).strip()

    words = text.split()

    words = [
        word for word in words
        if word not in stop_words
    ]

    words = [
        lemmatizer.lemmatize(word)
        for word in words
    ]

    return " ".join(words)


def predict_category(text):
    """
    Predict complaint category and confidence.
    """
    # 1. Fallback for empty input
    if not text or not str(text).strip():
        return {"category": "Uncategorized", "confidence": 0.0}

    # 2. Avoid double preprocessing if already cleaned
    # (If 'text' is already cleaned, pass it directly; otherwise clean it)
    cleaned_text = text if isinstance(text, str) and text.islower() else preprocess_for_model(text)

    # 3. Vectorize text
    text_vector = vectorizer.transform([cleaned_text])

    # 4. Debug Check: If vocabulary match failed, log it in terminal
    if text_vector.nnz == 0:
        print(f"[WARNING] Classifier vectorizer matching 0 words for text: '{cleaned_text}'")

    # 5. Predict class and probability
    predicted_category = model.predict(text_vector)[0]
    probabilities = model.predict_proba(text_vector)[0]
    confidence = float(np.max(probabilities))

    return {
        "category": str(predicted_category),
        "confidence": round(confidence, 2)
    }