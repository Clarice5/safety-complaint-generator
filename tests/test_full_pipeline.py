from app.pipeline.complaint_pipeline import (
    run_complaint_pipeline
)


complaint = (
    "Rahul threatened me near Borivali station "
    "on 15 August at 8 PM."
)


result = run_complaint_pipeline(
    complaint=complaint,
    language="English",
    date="15 August",
    time="8 PM",
    location="Borivali"
)


print("===== FULL PIPELINE TEST =====")

print("\nCategory:")
print(result["category"])

print("\nConfidence:")
print(result["confidence"])

print("\nEntities:")
print(result["entities"])

print("\nSimilar Complaints:")
for item in result["similar_complaints"]:
    print(item)

print("\nSafety Advice:")
print(result["safety_advice"])

print("\nFormal English:")
print(result["formal_english"])

print("\nFormal Hindi:")
print(result["formal_hindi"])

print("\nMongoDB Document ID:")
print(result["document_id"])