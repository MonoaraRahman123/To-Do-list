from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ..services import task_service

def api_login_required(view_func):
    """
    Middleware for API authentication.
    """
    def wrapper(request, *args, **kwargs):
        if "user_id" not in request.session:
            return JsonResponse({"error": "Unauthorized"}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper

@api_login_required
def api_tasks_list(request):
    """
    GET: List user tasks.
    """
    user_id = request.session["user_id"]
    tasks = task_service.get_tasks(user_id)
    # Convert tasks to serializable format (already handled in service for ObjectId)
    return JsonResponse({"tasks": tasks})

@csrf_exempt
@api_login_required
def api_task_detail(request, task_id):
    """
    GET: Get task details.
    PUT: Update task.
    DELETE: Delete task.
    """
    if request.method == "GET":
        task = task_service.get_task_by_id(task_id)
        if task:
            return JsonResponse(task)
        return JsonResponse({"error": "Not found"}, status=404)
        
    elif request.method == "PUT":
        data = json.loads(request.body)
        task_service.update_task(task_id, data)
        return JsonResponse({"message": "Task updated"})
        
    elif request.method == "DELETE":
        task_service.delete_task(task_id)
        return JsonResponse({"message": "Task deleted"})
        
    return JsonResponse({"error": "Method not allowed"}, status=405)
