import os
import sys
import django
from datetime import datetime, timedelta

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_todo_manager.settings')
django.setup()

from core.services import auth_service, task_service, profile_service

def insert_sample_data():
    print("Inserting sample data...")
    
    # 1. Create a sample user
    username = "student_test"
    email = "test@example.com"
    password = "password123"
    
    user_id, error = auth_service.register_user(username, email, password)
    
    if error:
        print(f"User might already exist: {error}")
        # Try to authenticate to get the user_id if already exists
        user = auth_service.authenticate_user(username, password)
        if user:
            user_id = user["_id"]
        else:
            print("Failed to get user_id.")
            return

    print(f"User created/found with ID: {user_id}")

    # 2. Update Profile
    profile_data = {
        "name": "Test Student",
        "email": email,
        "student_id": "S12345",
        "department": "Computer Science"
    }
    profile_service.create_or_update_profile(user_id, profile_data)
    print("Profile updated.")

    # 3. Create Sample Tasks
    tasks = [
        {
            "title": "Complete Django Project",
            "description": "Finish the Student To-Do Manager app with PyMongo.",
            "status": "pending",
            "priority": "high",
            "due_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
        },
        {
            "title": "Study for Finals",
            "description": "Review chapters 1-5 of Operating Systems.",
            "status": "pending",
            "priority": "medium",
            "due_date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        },
        {
            "title": "Submit Assignment 1",
            "description": "Database management system assignment.",
            "status": "completed",
            "priority": "high",
            "due_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        },
        {
            "title": "Gym Session",
            "description": "Don't forget leg day!",
            "status": "pending",
            "priority": "low",
            "due_date": datetime.now().strftime("%Y-%m-%d")
        }
    ]

    for t in tasks:
        task_service.create_task(user_id, t)
    
    print(f"Successfully inserted {len(tasks)} sample tasks.")
    print("\nLogin with:")
    print(f"Username: {username}")
    print(f"Password: {password}")

if __name__ == "__main__":
    insert_sample_data()
