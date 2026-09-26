from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017")

db = client["safety_complaints"]

complaints_collection = db["complaints"]


def save_complaint(complaint_data):
    """
    Save a complaint record in MongoDB.
    """

    result = complaints_collection.insert_one(
        complaint_data
    )

    return str(result.inserted_id)