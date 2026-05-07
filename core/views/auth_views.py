from django.shortcuts import render, redirect
from django.contrib import messages
from ..services import auth_service, profile_service

def login_view(request):
    """
    Handles user login.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = auth_service.authenticate_user(username, password)
        if user:
            # Set user info in session
            request.session["user_id"] = user["_id"]
            request.session["username"] = user["username"]
            messages.success(request, f"Welcome back, {username}!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, "core/login.html")

def register_view(request):
    """
    Handles user registration and initial profile creation.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        
        # Simple validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "core/register.html")
        
        user_id, error = auth_service.register_user(username, email, password)
        if user_id:
            # Create empty profile
            profile_service.create_or_update_profile(user_id, {
                "name": username,
                "email": email,
                "student_id": "",
                "department": ""
            })
            messages.success(request, "Registration successful! Please login.")
            return redirect("login")
        else:
            messages.error(request, error)
            
    return render(request, "core/register.html")

def logout_view(request):
    """
    Clears session and logs user out.
    """
    request.session.flush()
    messages.info(request, "You have been logged out.")
    return redirect("login")
