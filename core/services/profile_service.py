from .db import get_collection
from bson import ObjectId

profiles_col = get_collection("profiles")

def create_or_update_profile(user_id, profile_data):
    """
    Creates or updates a student profile for a given user.
    """
    profile_data["user_id"] = user_id
    
    # Use upsert to create if not exists, otherwise update
    result = profiles_col.update_one(
        {"user_id": user_id},
        {"$set": profile_data},
        upsert=True
    )
    return result

def get_profile(user_id):
    """
    Retrieves the profile for a specific user.
    """
    return profiles_col.find_one({"user_id": user_id})
