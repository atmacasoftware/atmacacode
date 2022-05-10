from django.urls import path
from adminpage.views import admin_main_page
urlpatterns = [
    path('',admin_main_page,name="admin_main_page")
]