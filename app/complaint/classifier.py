import os
import re
import string
import joblib
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Import translation helper for Hindi inputs
from app.translation.translator import translate_hindi_to_english

# Project root directory
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

MODEL_DIR = os.path.join(BASE_DIR, "models")

# Load trained model and vectorizer
vectorizer = joblib.load(
    os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
)

model = joblib.load(
    os.path.join(MODEL_DIR, "complaint_model.pkl")
)

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def is_devanagari(text: str) -> bool:
    """Check if string contains Devanagari (Hindi) script."""
    if not text:
        return False
    return bool(re.search(r"[\u0900-\u097F]", str(text)))


def preprocess_for_model(text: str) -> str:
    """Clean and lemmatize text for classification."""
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    words = text.split()
    words = [word for word in words if word not in stop_words]
    words = [lemmatizer.lemmatize(word) for word in words]

    return " ".join(words)


def predict_category(text: str) -> dict:
    """Predict complaint category and confidence score with Hindi auto-translation."""
    if not text or not str(text).strip():
        return {"category": "Uncategorized", "confidence": 0.0}

    # 1. If input contains Hindi Devanagari script, translate to English first
    classification_text = text
    if is_devanagari(text):
        try:
            translated = translate_hindi_to_english(text)
            # Ensure translation succeeded and returned clean English text
            if translated and not is_devanagari(translated):
                classification_text = translated
        except Exception as e:
            print(f"[ERROR] Translation failed during classification: {e}")

    # 2. Preprocess text prior to vectorization
    cleaned_text = preprocess_for_model(classification_text)

    # Fallback if preprocessing removes all words
    if not cleaned_text:
        return {"category": "Other", "confidence": 0.0}

    # 3. Vectorize text
    text_vector = vectorizer.transform([cleaned_text])

    # Guard against completely out-of-vocabulary inputs
    if text_vector.nnz == 0:
        print(f"[WARNING] Vectorizer matched 0 words for text: '{cleaned_text}'")
        return {"category": "Other", "confidence": 0.0}

    # 4. Predict class and probability
    predicted_category = model.predict(text_vector)[0]
    
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(text_vector)[0]
        confidence = float(np.max(probabilities))
    else:
        confidence = 1.0

    # Threshold low-confidence predictions
    final_category = str(predicted_category) if confidence >= 0.30 else "Other"

    return {
        "category": final_category,
        "confidence": round(confidence, 2)
    }