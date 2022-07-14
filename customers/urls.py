from django.urls import path
from customers.views import *
urlpatterns = [
    path("giris",Login.as_view(), name="customer_login"),
    path("kayit-ol",Signup.as_view(), name="customer_register"),
    path("<username>",profile_page, name="customer_profile"),
    path("cıkıs-yap",logout, name="customer_logout"),
    path("<username>/siparislerim",order_page, name="customer_order"),
    path("<username>/duyurular",announcement_page, name="customer_announcement"),
]