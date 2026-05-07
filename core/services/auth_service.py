from django.contrib.auth.hashers import make_password, check_password
from .db import get_collection
from bson import ObjectId

users_col = get_collection("users")

def register_user(username, email, password):
    """
    Registers a new user in MongoDB after hashing the password.
    """
    # Check if user already exists
    if users_col.find_one({"$or": [{"username": username}, {"email": email}]}):
        return None, "Username or Email already exists."
    
    # Hash password using Django's default hasher
    hashed_password = make_password(password)
    
    user_data = {
        "username": username,
        "email": email,
        "password": hashed_password
    }
    
    result = users_col.insert_one(user_data)
    return str(result.inserted_id), None

def authenticate_user(username, password):
    """
    Checks credentials and returns user data if valid.
    """
    user = users_col.find_one({"username": username})
    
    if user and check_password(password, user["password"]):
        # Remove password from user object before returning
        user["_id"] = str(user["_id"])
        del user["password"]
        return user
    
    return None

def get_user_by_id(user_id):
    """
    Retrieves user by MongoDB ObjectId.
    """
    user = users_col.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
        del user["password"]
    return user
