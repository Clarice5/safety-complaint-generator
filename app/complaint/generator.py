from datetime import datetime
import re
from app.translation.translator import (
    translate_hindi_to_english,
    translate_english_to_hindi
)


def is_devanagari(text: str) -> bool:
    """Check if string contains Devanagari (Hindi) script."""
    if not text:
        return False
    return bool(re.search(r"[\u0900-\u097F]", str(text)))


def format_date(date_str: str) -> str:
    if not date_str:
        return ""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d %B %Y").lstrip("0")
    except ValueError:
        return date_str


def format_time(time_str: str) -> str:
    if not time_str:
        return ""
    try:
        time_obj = datetime.strptime(time_str, "%H:%M")
        return time_obj.strftime("%I:%M %p").lstrip("0")
    except ValueError:
        return time_str


def generate_formal_complaint(
    original_complaint: str,
    category: str,
    entities: dict,
    language: str = "English",
    date: str = "",
    time: str = "",
    location: str = "",
    translated_complaint: str = ""
) -> dict:
    persons = entities.get("persons", [])
    locations = entities.get("locations", [])
    dates = entities.get("dates", [])
    times = entities.get("times", [])

    final_date = date or (dates[0] if dates else "the mentioned date")
    final_time = time or (times[0] if times else "the mentioned time")
    final_location = location or (locations[0] if locations else "the mentioned location")
    person = persons[0] if persons else ""

    readable_date = format_date(final_date)
    readable_time = format_time(final_time)

    # Use pre-translated text if provided, otherwise perform translation
    if translated_complaint and not is_devanagari(translated_complaint):
        english_details = translated_complaint
    elif is_devanagari(original_complaint):
        try:
            trans = translate_hindi_to_english(original_complaint)
            english_details = trans if (trans and not is_devanagari(trans)) else original_complaint
        except Exception:
            english_details = original_complaint
    else:
        english_details = original_complaint

    hindi_details = original_complaint if is_devanagari(original_complaint) else translate_english_to_hindi(original_complaint)

    # Category Mapping
    hindi_categories = {
        "Blackmail": "ब्लैकमेल",
        "Eve Teasing": "छेड़छाड़",
        "Harassment": "उत्पीड़न",
        "Domestic Violence": "घरेलू हिंसा",
        "Public Safety": "सार्वजनिक सुरक्षा",
        "Threat": "धमकी",
        "Stalking": "पीछा किए जाने",
        "Cyber Harassment": "साइबर उत्पीड़न",
        "Theft": "चोरी",
        "Uncategorized": "अज्ञात/अन्य",
        "Other": "अन्य"
    }

    hindi_category = hindi_categories.get(category, "अन्य")
    display_category_en = "an unspecified incident" if category.lower() in ["uncategorized", "other"] else category.lower()

    # Location in both languages. Detect the script directly rather than
    # trusting the `language` dropdown, since `final_location` may instead
    # come from an entity extracted out of the original complaint text.
    if final_location == "the mentioned location":
        english_location = final_location
        hindi_location = "उल्लेखित स्थान"
    elif is_devanagari(final_location):
        hindi_location = final_location
        try:
            trans = translate_hindi_to_english(final_location)
            english_location = trans if (trans and not is_devanagari(trans)) else final_location
        except Exception:
            english_location = final_location
    else:
        english_location = final_location
        try:
            trans = translate_english_to_hindi(final_location)
            hindi_location = trans if trans else final_location
        except Exception:
            hindi_location = final_location

    # --- Build Formal English Complaint ---
    # Filter out person entities containing Devanagari characters
    person_en = ""
    if person and not is_devanagari(person):
        person_en = person

    english_complaint = (
        f"I would like to formally report an incident involving {display_category_en}. "
        f"The incident occurred at {english_location} on {readable_date} at {readable_time}. "
    )
    if person_en:
        english_complaint += f"The incident involves {person_en}. "

    english_complaint += (
        f"The details of the incident are as follows: {english_details} "
        f"I request that this matter be investigated and appropriate action be taken."
    )

    # --- Build Formal Hindi Complaint ---
    hindi_date = readable_date
    hindi_time = readable_time

    hindi_months = {
        "January": "जनवरी", "February": "फरवरी", "March": "मार्च",
        "April": "अप्रैल", "May": "मई", "June": "जून",
        "July": "जुलाई", "August": "अगस्त", "September": "सितंबर",
        "October": "अक्टूबर", "November": "नवंबर", "December": "दिसंबर"
    }

    for en_m, hi_m in hindi_months.items():
        hindi_date = hindi_date.replace(en_m, hi_m)

    hindi_time = hindi_time.replace("AM", "पूर्वाह्न").replace("PM", "अपराह्न")

    hindi_complaint = (
        f"मैं {hindi_category} की घटना के संबंध में एक औपचारिक शिकायत दर्ज करना चाहता/चाहती हूँ। "
        f"यह घटना {hindi_date} को {hindi_time} बजे {hindi_location} में हुई। "
    )

    hindi_complaint += (
        f"घटना का विवरण इस प्रकार है: {hindi_details} "
        f"अतः मेरा अनुरोध है कि इस मामले की जांच की जाए और उचित कार्रवाई की जाए।"
    )

    return {
        "formal_english": english_complaint.strip(),
        "formal_hindi": hindi_complaint.strip()
    }