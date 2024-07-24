from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.models import auth
from app.models import Product
from email.message import EmailMessage
import smtplib

# Create your views here.
User = get_user_model()

def home(request):
    msg = EmailMessage()
    email_Address = '........'
    email_password = 'rvryltoqgvuvtrjh'
    msg.set_content("Hello World")
    msg["Subject"] = "Test mail"
    msg['From'] = '...........'
    msg['To'] = 'ayodejiadeyemo795@gmail.com'
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_Address, email_password)
        smtp.send_message(msg)

    all_products = Product.objects.all().order_by("-created_at")
    context = {'products': all_products}
    # if request.method == "POST":
    #     name = request.POST.get("name")
    #     message = request.POST.get("message")
    #     email = request.POST.get("email")
    #     body = 

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


def create_product(request):
    user = request.user
    if not user.is_authenticated:
        return redirect(login)
    
    if request.method == "POST":
        title = request.POST.get("title")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        image = request.POST.get("image")
        if not title or not price or not quantity or not image:
            messages.error(request, "All fields are required")
            return render(request, "app/new_product.html")
        new_product = Product.objects.create(
            title = title,
            price = price,
            quantity = quantity,
            picture = image,
            owner = user
        )
        new_product.save()
        messages.success(request, "Created succesfully")
        return redirect(dashboard)
    return render(request, "app/new_product.html")

def edit_product(request, id):
    user= request.user
    if not user.is_authenticated:
        return redirect(login)
    product = Product.objects.filter(id=id).first()
    if not product:
        messages.error(request, "No product with such ID")
        return redirect(home)
    if product.owner != user:
        return redirect(home)
    if request.method == 'POST':
        title = request.POST.get("title")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        image = request.POST.get("image")

        product.title = title
        product.price = price
        product.quantity = quantity
        if image:
            product.image = image
        product.save()
        messages.success(request, "Product successfuly modified")
    return render(request, "app/edit_product.html", {"product": product})


def single_product(request, id):
    user = request.user
    if not user.is_authenticated:
        return redirect(login)
    product = Product.objects.filter(id=id).first()
    if not product:
        messages.error(request, "No product with such ID")
        return redirect(home)
    if request.method == "POST":
        quantity = request.POST.get("quantity")
        if not quantity:
            messages.error(request, "Quantity not provided")
            return redirect(home)
        quantity = int(quantity)
        if product.quantity < quantity:
            messages.error(request, "More than quantiy available")
            return redirect(home)
        product.quantity -= quantity
        if product.quantity == 0:
            product.is_active = False
        product.save()
        messages.success(request, "Purchase done")
        return redirect(home)
    
    context = {"product": product}
    return render(request, "app/single_product.html", context)


def deleteProduct(request, id):
    user= request.user
    if not user.is_authenticated:
        return redirect(login)
    product = Product.objects.filter(id=id).first()
    if not product:
        messages.error(request, "No product with such ID")
        return redirect(home)
    if product.owner != user:
        return redirect(home)
    product.delete()
    messages.success(request, "Purchase deleted successfully")
    return redirect(home)