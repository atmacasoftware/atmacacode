from django.shortcuts import render

# Create your views here.

def admin_main_page(request):
    return render(request, "adminpage/mainpage.html")
