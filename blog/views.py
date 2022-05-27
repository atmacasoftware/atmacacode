from django.shortcuts import render
from blog.models import Blog
# Create your views here.

def blog_page(request):
    mainblog = Blog.objects.filter(is_main_slider=True)[:10]
    return render(request,"mainpage/blog.html",{'mainblog':mainblog})

def blog_details(request,slug):
    blog_detail = None
    try:
        blog_detail = Blog.objects.get(slug=slug)
    except:
        pass
    return render(request,'mainpage/blog_details.html',{'blog_detail':blog_detail})

