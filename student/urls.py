from django.urls import path
from student.views import *

urlpatterns = [
    path('', dashboard, name='student_dashboard'),
]