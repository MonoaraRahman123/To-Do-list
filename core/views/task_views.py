from django.shortcuts import render, redirect
from django.contrib import messages
from ..services import task_service, profile_service

def login_required_custom(view_func):
    """
    Custom decorator to check if user is logged in via session.
    """
    def wrapper(request, *args, **kwargs):
        if "user_id" not in request.session:
            messages.warning(request, "Please login to access this page.")
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required_custom
def dashboard_view(request):
    """
    Displays user tasks and statistics.
    """
    user_id = request.session["user_id"]
    
    # Get filters from GET parameters
    filters = {
        "status": request.GET.get("status"),
        "priority": request.GET.get("priority")
    }
    
    tasks = task_service.get_tasks(user_id, filters)
    stats = task_service.get_task_stats(user_id)
    
    context = {
        "tasks": tasks,
        "stats": stats,
        "current_filters": filters
    }
    return render(request, "core/dashboard.html", context)

@login_required_custom
def create_task_view(request):
    """
    Handles task creation.
    """
    if request.method == "POST":
        task_data = {
            "title": request.POST.get("title"),
            "description": request.POST.get("description"),
            "status": "pending",
            "priority": request.POST.get("priority"),
            "due_date": request.POST.get("due_date")
        }
        task_service.create_task(request.session["user_id"], task_data)
        messages.success(request, "Task created successfully!")
        return redirect("dashboard")
        
    return render(request, "core/task_form.html", {"action": "Create"})

@login_required_custom
def update_task_view(request, task_id):
    """
    Handles task updates.
    """
    task = task_service.get_task_by_id(task_id)
    if not task:
        messages.error(request, "Task not found.")
        return redirect("dashboard")
        
    if request.method == "POST":
        task_data = {
            "title": request.POST.get("title"),
            "description": request.POST.get("description"),
            "status": request.POST.get("status"),
            "priority": request.POST.get("priority"),
            "due_date": request.POST.get("due_date")
        }
        task_service.update_task(task_id, task_data)
        messages.success(request, "Task updated successfully!")
        return redirect("dashboard")
        
    # Format date for input field
    if task.get("due_date"):
        task["due_date"] = task["due_date"].strftime("%Y-%m-%d")
        
    return render(request, "core/task_form.html", {"task": task, "action": "Update"})

@login_required_custom
def delete_task_view(request, task_id):
    """
    Handles task deletion.
    """
    task_service.delete_task(task_id)
    messages.success(request, "Task deleted.")
    return redirect("dashboard")

@login_required_custom
def profile_view(request):
    """
    Handles student profile management.
    """
    user_id = request.session["user_id"]
    if request.method == "POST":
        profile_data = {
            "name": request.POST.get("name"),
            "email": request.POST.get("email"),
            "student_id": request.POST.get("student_id"),
            "department": request.POST.get("department")
        }
        profile_service.create_or_update_profile(user_id, profile_data)
        messages.success(request, "Profile updated successfully!")
        return redirect("profile")
        
    profile = profile_service.get_profile(user_id)
    return render(request, "core/profile.html", {"profile": profile})
