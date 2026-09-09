from app.translation.translator import translate_hindi_to_english, translate_english_to_hindi
from datetime import datetime


def format_date(date):
    """Convert YYYY-MM-DD into a readable date."""
    if not date:
        return ""

    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        return date_obj.strftime("%d %B %Y").lstrip("0")
    except ValueError:
        return date


def format_time(time):
    """Convert HH:MM into 12-hour AM/PM format."""
    if not time:
        return ""

    try:
        time_obj = datetime.strptime(time, "%H:%M")
        return time_obj.strftime("%I:%M %p").lstrip("0")
    except ValueError:
        return time


def generate_formal_complaint(
    original_complaint,
    category,
    entities,
    language="English",
    date="",
    time="",
    location=""
):
    persons = entities.get("persons", [])
    locations = entities.get("locations", [])
    dates = entities.get("dates", [])
    times = entities.get("times", [])

    # Prefer information entered in the website form.
    final_date = date or (dates[0] if dates else "the mentioned date")
    final_time = time or (times[0] if times else "the mentioned time")
    final_location = location or (
        locations[0] if locations else "the mentioned location"
    )

    person = persons[0] if persons else "the concerned person"

    # Make website date/time readable.
    readable_date = format_date(final_date)
    readable_time = format_time(final_time)

    hindi_categories = {
        "Blackmail": "ब्लैकमेल",
        "Eve Teasing": "छेड़छाड़",
        "Harassment": "उत्पीड़न",
        "Domestic Violence": "घरेलू हिंसा",
        "Public Safety": "सार्वजनिक सुरक्षा",
        "Threat": "धमकी",
        "Stalking": "पीछा करना",
        "Cyber Harassment": "साइबर उत्पीड़न",
        "Theft": "चोरी",
        "Other": "अन्य"
    }

    hindi_category = hindi_categories.get(category, "अन्य")

    # Prepare complaint details in both languages.
    if language.lower() == "hindi":
        hindi_details = original_complaint
        english_details = translate_hindi_to_english(original_complaint)
    else:
        english_details = original_complaint
        hindi_details = translate_english_to_hindi(original_complaint)

    # -------------------------
    # Formal English Complaint
    # -------------------------

    english_complaint = (
        f"I would like to formally report an incident involving {category.lower()}. "
        f"The incident occurred at {final_location} on {readable_date} "
        f"at {readable_time}. "
        f"The incident involves {person}. "
        f"The details of the incident are as follows: "
        f"{english_details} "
        f"I request that this matter be investigated and appropriate action be taken."
    )

    # -------------------------
    # Formal Hindi Complaint
    # -------------------------

    hindi_date = readable_date
    hindi_time = readable_time

    # Convert English month names into Hindi.
    hindi_months = {
        "January": "जनवरी",
        "February": "फरवरी",
        "March": "मार्च",
        "April": "अप्रैल",
        "May": "मई",
        "June": "जून",
        "July": "जुलाई",
        "August": "अगस्त",
        "September": "सितंबर",
        "October": "अक्टूबर",
        "November": "नवंबर",
        "December": "दिसंबर"
    }

    for english_month, hindi_month in hindi_months.items():
        hindi_date = hindi_date.replace(
            english_month,
            hindi_month
        )

    # Convert AM/PM into Hindi.
    hindi_time = hindi_time.replace("AM", "पूर्वाह्न")
    hindi_time = hindi_time.replace("PM", "अपराह्न")

    # Translate location and person for the Hindi complaint.
    hindi_location = final_location
    hindi_person = person

    if final_location:
        translated_location = translate_english_to_hindi(final_location)
        if translated_location:
            hindi_location = translated_location

    if person and person != "the concerned person":
        translated_person = translate_english_to_hindi(person)
        if translated_person:
            hindi_person = translated_person

    # Hindi complaint details are already translated above.
    hindi_complaint = (
        f"मैं {hindi_category} से संबंधित एक घटना की औपचारिक शिकायत दर्ज "
        f"करना चाहता/चाहती हूँ। "
        f"यह घटना {hindi_date} को {hindi_time} बजे "
        f"{hindi_location} पर हुई। "
        f"इस घटना में {hindi_person} शामिल है। "
        f"घटना का विवरण इस प्रकार है: "
        f"{hindi_details} "
        f"अतः मेरा अनुरोध है कि इस मामले की जांच की जाए और उचित कार्रवाई की जाए।"
    )

    return {
        "formal_english": english_complaint,
        "formal_hindi": hindi_complaint
    }