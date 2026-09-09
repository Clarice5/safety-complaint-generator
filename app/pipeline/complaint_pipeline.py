from datetime import datetime

from app.pipeline.text_pipeline import process_complaint
from app.ner.entity_extraction import extract_entities
from app.complaint.advice import get_safety_advice
from app.complaint.generator import generate_formal_complaint
from app.similarity.complaint_similarity import find_similar_complaints
from app.database.mongodb import save_complaint


def predict_category(text):
    """
    Temporary classifier.

    This will later be replaced by Anaya's ML model.
    """

    return {
        "category": "Threat",
        "confidence": 0.92
    }


def run_complaint_pipeline(
    complaint,
    language,
    date="",
    time="",
    location=""
):
    """
    Run the complete complaint processing pipeline.
    """

    # 1. Process language and text
    processed = process_complaint(
        complaint,
        language
    )

    # 2. Get English text for ML and similarity
    english_text = processed["translated_text"]

    # 3. Extract entities
    entities = extract_entities(
        english_text
    )

    # 4. Predict complaint category
    prediction = predict_category(
        processed["english_processed"]
    )

    category = prediction["category"]
    confidence = prediction["confidence"]

    # 5. Find similar historical complaints
    similar_complaints = find_similar_complaints(
        english_text,
        category=category,
        top_n=5
    )

    # 6. Get Hindi safety advice
    safety_advice = get_safety_advice(
        category
    )

    # 7. Generate formal complaints
    formal_complaints = generate_formal_complaint(
        original_complaint=complaint,
        category=category,
        entities=entities,
        language=language,
        date=date,
        time=time,
        location=location
    )

    # 8. Create complete MongoDB record
    complaint_record = {
        "original_complaint": complaint,
        "language": language,

        "hindi_processed": processed[
            "hindi_processed"
        ],

        "translated_complaint": processed[
            "translated_text"
        ],

        "english_processed": processed[
            "english_processed"
        ],

        "date": date,
        "time": time,
        "location": location,

        "category": category,
        "confidence": confidence,

        "entities": entities,

        "similar_complaints": similar_complaints,

        "safety_advice": safety_advice,

        "formal_english": formal_complaints[
            "formal_english"
        ],

        "formal_hindi": formal_complaints[
            "formal_hindi"
        ],

        "created_at": datetime.now()
    }

    # 9. Save complete record
    document_id = save_complaint(
        complaint_record
    )

    # 10. Return everything to the application
    complaint_record["document_id"] = document_id

    return complaint_record