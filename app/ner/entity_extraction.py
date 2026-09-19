import spacy
import re

nlp = spacy.load("en_core_web_sm")


def extract_entities(text):
    """
    Extract persons, locations, organizations, dates and times.
    """

    if not isinstance(text, str) or not text.strip():
        return {
            "persons": [],
            "locations": [],
            "organizations": [],
            "dates": [],
            "times": []
        }

    doc = nlp(text)

    entities = {
        "persons": [],
        "locations": [],
        "organizations": [],
        "dates": [],
        "times": []
    }

    # Standard frequency expressions to exclude from DATE entities
    frequency_terms = [
        "every day",
        "every week",
        "every month",
        "daily",
        "weekly",
        "monthly",
        "each day",
        "each week",
        "each month"
    ]

    # Extract spaCy entities
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            entities["persons"].append(ent.text)
        elif ent.label_ in ["GPE", "LOC", "FAC"]:
            entities["locations"].append(ent.text)
        elif ent.label_ == "ORG":
            entities["organizations"].append(ent.text)
        elif ent.label_ == "DATE":
            if ent.text.lower().strip() not in frequency_terms:
                entities["dates"].append(ent.text)
        elif ent.label_ == "TIME":
            entities["times"].append(ent.text)

    # ------------------------------------------------
    # Fallback for person names (Updated to catch all matches)
    # ------------------------------------------------
    person_matches = re.finditer(
        r"\b([A-Z][a-z]+)\s+"
        r"(?:threatened|harassed|stalked|attacked|followed)"
        r"\b",
        text
    )

    for match in person_matches:
        person = match.group(1)
        if person not in entities["persons"]:
            entities["persons"].insert(0, person)

    # ------------------------------------------------
    # Fallback for location after "near" (Updated to catch all matches)
    # ------------------------------------------------
    location_matches = re.finditer(
        r"\bnear\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
        text
    )

    for match in location_matches:
        location = match.group(1)
        # Remove words that obviously aren't location names
        location = re.split(
            r"\s+(?:on|at|in|for|and)\b",
            location
        )[0].strip()

        if location and location not in entities["locations"]:
            entities["locations"].insert(0, location)

    # Remove entities that are already identified as locations
    entities["persons"] = [
        person
        for person in entities["persons"]
        if person not in entities["locations"]
    ]

    return entities