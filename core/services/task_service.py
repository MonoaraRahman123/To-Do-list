from .db import get_collection
from bson import ObjectId
from datetime import datetime

tasks_col = get_collection("tasks")

def create_task(user_id, task_data):
    """
    Creates a new task for a user.
    """
    task_data["user_id"] = user_id
    task_data["created_at"] = datetime.now()
    if "due_date" in task_data and task_data["due_date"]:
        task_data["due_date"] = datetime.strptime(task_data["due_date"], "%Y-%m-%d")
    
    result = tasks_col.insert_one(task_data)
    return str(result.inserted_id)

def get_tasks(user_id, filters=None):
    """
    Retrieves tasks for a user with optional filtering.
    """
    query = {"user_id": user_id}
    if filters:
        if filters.get("status"):
            query["status"] = filters["status"]
        if filters.get("priority"):
            query["priority"] = filters["priority"]
    
    tasks = list(tasks_col.find(query).sort("due_date", 1))
    for task in tasks:
        task["id"] = str(task["_id"])
    return tasks

def get_task_by_id(task_id):
    """
    Retrieves a single task by its ObjectId.
    """
    task = tasks_col.find_one({"_id": ObjectId(task_id)})
    if task:
        task["id"] = str(task["_id"])
    return task

def update_task(task_id, task_data):
    """
    Updates an existing task.
    """
    if "due_date" in task_data and task_data["due_date"] and isinstance(task_data["due_date"], str):
        task_data["due_date"] = datetime.strptime(task_data["due_date"], "%Y-%m-%d")
        
    result = tasks_col.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": task_data}
    )
    return result.modified_count

def delete_task(task_id):
    """
    Deletes a task from MongoDB.
    """
    result = tasks_col.delete_one({"_id": ObjectId(task_id)})
    return result.deleted_count

def get_task_stats(user_id):
    """
    Returns counts for total, completed, and pending tasks.
    """
    total = tasks_col.count_documents({"user_id": user_id})
    completed = tasks_col.count_documents({"user_id": user_id, "status": "completed"})
    pending = tasks_col.count_documents({"user_id": user_id, "status": "pending"})
    
    return {
        "total": total,
        "completed": completed,
        "pending": pending
    }
