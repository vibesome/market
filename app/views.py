from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.models import auth

# Create your views here.
User = get_user_model()

def home(request):
    context = {}
    return render(request, "app/home.html", context)

def signup(request):
    user = request.user
    if user.is_authenticated:
        return redirect(dashboard)
    if request.method == "POST":
        username = request.POST.get("username")
        if not username:
            messages.error(request, "Username is compulsory")
            return render(request, "app/signup.html")
        email = request.POST.get("email")
        if not email:
            messages.error(request, "Email is compulsory")
            return render(request, "app/signup.html")
        password = request.POST.get("password")
        if not password:
            messages.error(request, "Password is compulsory")
            return render(request, "app/signup.html")
        
        if len(password) < 8:
            messages.error(request, "Password must be up to 8 character")
            return render(request, "app/signup.html")
        cpassword = request.POST.get("cpassword")
        if password != cpassword:
            messages.error(request, "Password did not match")
            return render(request, "app/signup.html")
        username_already_taken = User.objects.filter(username=username).exists()
        if username_already_taken:
            messages.error(request, "Username already taken")
            return render(request, "app/signup.html")
        
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            messages.error(request, "Email already taken")
            return render(request, "app/signup.html")
        new_user = User.objects.create(
            username = username,
            email=email
        )
        new_user.set_password(password)
        new_user.save()
        messages.success(request, "Account created, please login")
        return redirect(login)


    return render(request, "app/signup.html")



def login(request):
    user = request.user
    if user.is_authenticated:
        return redirect(dashboard)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not username or not password:
            messages.error(request, "Invalid details")
            return render(request, "app/login.html")
        user = auth.authenticate(username=username, password=password)
        if not user:
            messages.error(request, "Invalid login credentials")
            return render(request, "app/login.html")
        auth.login(request, user)
        return redirect(dashboard)
    return render(request, "app/login.html")




def dashboard(request):
    user = request.user
    if not user.is_authenticated:
        return redirect(login)
    return render(request, "app/dashboard.html")


def logout(request):
    auth.logout(request)
    return redirect(login)