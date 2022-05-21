from django.shortcuts import render
from user_accounts.models import Account
# Create your views here.

def index(request):
    return render(request, "mainpage/mainpage.html")


