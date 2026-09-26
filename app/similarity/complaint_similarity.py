import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.preprocessing.english_preprocessing import preprocess_english


def find_similar_complaints(
    complaint,
    dataset_path="dataset/english_dataset.csv",
    category=None,
    top_n=5
):
    """
    Find historically similar complaints using
    TF-IDF and cosine similarity.

    If a category is provided, similarity is calculated
    only against complaints from that category.
    """

    # Load historical complaints
    df = pd.read_csv(dataset_path)

    # Check required columns
    if "complaint" not in df.columns or "category" not in df.columns:
        raise ValueError(
            "Dataset must contain 'complaint' and 'category' columns."
        )

    # Remove missing complaints
    df = df.dropna(subset=["complaint"]).copy()

    # Filter by predicted category
    if category is not None:

        df = df[
            df["category"].str.lower() == category.lower()
        ].copy()

    # If no complaints are available
    if df.empty:
        return []

    # Preprocess historical complaints
    df["processed_complaint"] = df["complaint"].apply(
        preprocess_english
    )

    # Preprocess new complaint
    processed_complaint = preprocess_english(
        complaint
    )

    # Historical complaints
    historical_complaints = df[
        "processed_complaint"
    ].tolist()

    # Add new complaint
    all_complaints = historical_complaints + [
        processed_complaint
    ]

    # TF-IDF
    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(
        all_complaints
    )

    # Cosine similarity
    similarity_scores = cosine_similarity(
        tfidf_matrix[-1],
        tfidf_matrix[:-1]
    ).flatten()

    # Add similarity scores
    df["similarity_score"] = similarity_scores

    # Sort highest similarity first
    similar_complaints = df.sort_values(
        by="similarity_score",
        ascending=False
    ).head(top_n)

    # Prepare results
    results = []

    for _, row in similar_complaints.iterrows():

        results.append({
            "complaint": row["complaint"],
            "category": row["category"],
            "similarity_score": round(
                float(row["similarity_score"]),
                4
            )
        })

    return results