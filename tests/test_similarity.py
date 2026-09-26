from app.similarity.complaint_similarity import (
    find_similar_complaints
)


complaint = (
    "My neighbor threatened me and sent abusive messages."
)


print("===== COMPLAINT SIMILARITY TEST =====")

print("\nNew Complaint:")
print(complaint)

results = find_similar_complaints(
    complaint,
    category="Threat",
    top_n=5
)

print("\n--- Similar Historical Complaints ---")

for i, result in enumerate(results, start=1):

    print(f"\n{i}.")
    print("Complaint:", result["complaint"])
    print("Category:", result["category"])
    print("Similarity:", result["similarity_score"])