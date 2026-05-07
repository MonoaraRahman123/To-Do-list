from django.urls import path
from .views import auth_views, task_views, api_views

urlpatterns = [
    # Auth URLs
    path("login/", auth_views.login_view, name="login"),
    path("register/", auth_views.register_view, name="register"),
    path("logout/", auth_views.logout_view, name="logout"),
    
    # Task URLs
    path("", task_views.dashboard_view, name="dashboard"),
    path("task/new/", task_views.create_task_view, name="create_task"),
    path("task/edit/<str:task_id>/", task_views.update_task_view, name="edit_task"),
    path("task/delete/<str:task_id>/", task_views.delete_task_view, name="delete_task"),
    
    # Profile URL
    path("profile/", task_views.profile_view, name="profile"),
    
    # API URLs
    path("api/tasks/", api_views.api_tasks_list, name="api_tasks"),
    path("api/tasks/<str:task_id>/", api_views.api_task_detail, name="api_task_detail"),
]
