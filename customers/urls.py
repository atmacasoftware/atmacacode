from django.urls import path
from customers.views import *
urlpatterns = [
    path("giris",customer_login, name="customer_login"),
    path("kayit-ol",customer_register, name="customer_register"),
]