from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.
from django.views import View


def admin_main_page(request):
    return render(request, "adminpage/signin.html")


