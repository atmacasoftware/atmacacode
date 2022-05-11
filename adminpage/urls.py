from django.urls import path
from adminpage.views import admin_main_page, SigninAdmin, SignupAdmin

urlpatterns = [
    path('',admin_main_page,name="admin_main_page"),
    path('yonetim-paneli-giris/',SigninAdmin.as_view(),name="admin_login"),
    path('yonetim-paneli-kayit/',SignupAdmin.as_view(),name="admin_register"),
]