from app.ner.entity_extraction import extract_entities


complaint = (
    "Rahul threatened me near Borivali station on 15 August "
    "at 8 PM. He works at ABC Company."
)


print("===== NER ENTITY EXTRACTION TEST =====")

print("\nComplaint:")
print(complaint)

entities = extract_entities(complaint)

print("\nExtracted Entities:")

for entity_type, values in entities.items():
    print(f"{entity_type}: {values}")