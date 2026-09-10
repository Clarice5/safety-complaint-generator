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


    # Extract spaCy entities

    for ent in doc.ents:

        if ent.label_ == "PERSON":

            entities["persons"].append(ent.text)

        elif ent.label_ in ["GPE", "LOC", "FAC"]:

            entities["locations"].append(ent.text)

        elif ent.label_ == "ORG":

            entities["organizations"].append(ent.text)

        elif ent.label_ == "DATE":
    # Ignore frequency expressions that spaCy may classify as dates
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

    if ent.text.lower().strip() not in frequency_terms:
        entities["dates"].append(ent.text)

    elif ent.label_ == "TIME":

         entities["times"].append(ent.text)


    # ------------------------------------------------
    # Fallback for person names
    # ------------------------------------------------

    person_pattern = re.search(
        r"\b([A-Z][a-z]+)\s+"
        r"(?:threatened|harassed|stalked|attacked|followed)"
        r"\b",
        text
    )

    if person_pattern:

        person = person_pattern.group(1)

        if person not in entities["persons"]:

            entities["persons"].insert(0, person)


    # ------------------------------------------------
    # Fallback for location after "near"
    # ------------------------------------------------

    location_pattern = re.search(
        r"\bnear\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
        text
    )

    if location_pattern:

        location = location_pattern.group(1)

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