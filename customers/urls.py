from django.urls import path
from customers.views import *
urlpatterns = [
    path("giris",Login.as_view(), name="customer_login"),
    path("kayit-ol",Signup.as_view(), name="customer_register"),
    path("profile/<username>",profile_page, name="customer_profile"),
]