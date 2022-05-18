from django.urls import path
from adminpage.views import admin_main_page, SigninAdmin, SignupAdmin,calender_page,add_task,logout,task_page,task_detail_page

urlpatterns = [
    path('yonetim-paneli/<username>/',admin_main_page,name="admin_main_page"),
    path('yonetim-paneli-giris/',SigninAdmin.as_view(),name="admin_login"),
    path('yonetim-paneli-kayit/',SignupAdmin.as_view(),name="admin_register"),
    path('takvim',calender_page,name="calender"),
    path('gorev-ekle/<username>/',add_task,name="add_task"),
    path('cikis-yap/',logout,name="logout"),
    path('gorevler/<username>/',task_page,name="task_page"),
    path('gorev/<int:task_id>/<username>/',task_detail_page,name="task_detail_page"),
]