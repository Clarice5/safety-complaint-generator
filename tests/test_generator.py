from app.complaint.generator import generate_formal_complaint


complaint = (
    "Rahul threatened me near Borivali station "
    "on 15 August at 8 PM."
)

category = "Threat"

entities = {
    "persons": ["Rahul"],
    "locations": ["Borivali"],
    "organizations": [],
    "dates": ["15 August"],
    "times": ["8 PM"]
}


result = generate_formal_complaint(
    original_complaint=complaint,
    category=category,
    entities=entities,
    date="15 August",
    time="8 PM",
    location="Borivali"
)


print("===== FORMAL COMPLAINT GENERATOR TEST =====")

print("\n--- Formal English Complaint ---")
print(result["formal_english"])

print("\n--- Formal Hindi Complaint ---")
print(result["formal_hindi"])