from django.urls import path
from adminpage.views import admin_main_page, SigninAdmin, SignupAdmin,calender_page

urlpatterns = [
    path('',admin_main_page,name="admin_main_page"),
    path('yonetim-paneli-giris/',SigninAdmin.as_view(),name="admin_login"),
    path('yonetim-paneli-kayit/',SignupAdmin.as_view(),name="admin_register"),
    path('takvim',calender_page,name="calender"),
]