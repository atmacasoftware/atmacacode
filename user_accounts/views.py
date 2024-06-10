from django.shortcuts import render
from user_accounts.models import User
# Create your views here.

def user_count(request):
    user_count = User.objects.all().count()
    student_count = User.objects.filter(is_student=True).count()
    customer_count = User.objects.filter(is_customer=True).count()
    admin_count = User.objects.filter(is_superuser=True).count()

    data = {'user_count':user_count, 'student_count':student_count, 'customer_count':customer_count, 'admin_count':admin_count}

    return data
