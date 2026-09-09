from app.database.mongodb import save_complaint


complaint_data = {
    "original_complaint": "Rahul threatened me near Borivali station.",
    "language": "English",

    "date": "15 August",
    "time": "8 PM",
    "location": "Borivali",

    "category": "Threat",
    "confidence": 0.92,

    "entities": {
        "persons": ["Rahul"],
        "locations": ["Borivali"],
        "organizations": [],
        "dates": ["15 August"],
        "times": ["8 PM"]
    },

    "safety_advice": (
        "यदि आपको खतरा महसूस हो रहा है, "
        "तो सुरक्षित स्थान पर जाएं और "
        "विश्वसनीय व्यक्ति से सहायता लें।"
    ),

    "formal_english": (
        "I would like to formally report an incident "
        "related to threats."
    ),

    "formal_hindi": (
        "मैं धमकी से संबंधित एक घटना की "
        "औपचारिक शिकायत दर्ज करना चाहता/चाहती हूँ।"
    )
}


inserted_id = save_complaint(complaint_data)

print("Complete complaint saved successfully!")
print("Document ID:", inserted_id)