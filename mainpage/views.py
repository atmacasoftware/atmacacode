from django.shortcuts import render

from blog.models import Blog
from products.models import Services
from user_accounts.models import Account
# Create your views here.

def index(request):
    blog = None
    services = None
    try:
        blog = Blog.objects.all()[:3]
    except:
        pass
    try:
        services = Services.objects.all()
    except:
        pass
    return render(request, "mainpage/mainpage.html",{'blog':blog,'services':services})


