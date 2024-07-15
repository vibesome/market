from django.urls import path
from app.views import *

urlpatterns = [
    path('', home, name='home'),
    path('signup', signup, name='signup'),
    path('login', login, name='login'),
    path('dashboard', dashboard, name='dashboard'),
    path('logout', logout, name='logout'),
    path('create_product', create_product, name='create_product'),
    path('single_product/<str:id>', single_product, name="single_product")
]
