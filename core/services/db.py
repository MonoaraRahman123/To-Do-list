import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get MongoDB configuration from environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "student_todo_db")

# Initialize MongoDB client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def get_db():
    """
    Returns the MongoDB database instance.
    """
    return db

def get_collection(collection_name):
    """
    Returns a specific collection from the database.
    """
    return db[collection_name]
