from django.urls import path
from customers.views import *


urlpatterns = [
    path("giris",Login.as_view(), name="customer_login"),
    path("kayit-ol",Signup.as_view(), name="customer_register"),
    path("duzenleme/<username>",profile_page, name="customer_profile"),
    path("cıkıs-yap",logout, name="customer_logout"),
    path("siparislerim/<username>",order_page, name="customer_order"),
    path("duyurular/<username>",announcement_page, name="customer_announcement"),
    path("duyurular/<username>/<int:id>",read_announcement_page, name="read_announcement_page"),
    path("duyurular/<username>/<int:id>/sil",delete_announcement_page, name="delete_announcement_page"),
    path("<username>/destek-taleplerim",support_page, name="create_support"),
    path("<username>/destek-taleplerim/<int:room_id>",support_page_message, name="support_page_message"),
]