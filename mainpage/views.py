from django.shortcuts import render

from blog.models import Blog
from user_accounts.models import Account
# Create your views here.

def index(request):
    blog = None
    try:
        blog = Blog.objects.all()[:3]
    except:
        pass
    return render(request, "mainpage/mainpage.html",{'blog':blog})


