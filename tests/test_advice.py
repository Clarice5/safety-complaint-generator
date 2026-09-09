from app.complaint.advice import get_safety_advice


categories = [
    "Blackmail",
    "Eve Teasing",
    "Harassment",
    "Domestic Violence",
    "Public Safety",
    "Threat",
    "Stalking",
    "Cyber Harassment",
    "Theft",
    "Other"
]


print("===== SAFETY ADVICE TEST =====")

for category in categories:

    advice = get_safety_advice(category)

    print(f"\nCategory: {category}")
    print(f"Advice: {advice}")