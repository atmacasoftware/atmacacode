from django.shortcuts import render
from blog.models import Blog
# Create your views here.
from social_media.models import Instagram


def blog_page(request):
    mainblog = None
    single_blog = None
    recent_blog = None
    instagram_image = None
    blog_count = None
    try:
        mainblog = Blog.objects.filter(is_main_slider=True)[:10]
    except:
        pass
    try:
        single_blog = Blog.objects.filter()[:10]
    except:
        pass
    try:
        recent_blog = Blog.objects.filter().order_by("-id")[:5]
    except:
        pass
    try:
        instagram_image = Instagram.objects.all().order_by("-id")[:6]
    except:
        pass
    try:
        blog_count = Blog.objects.all().count()
    except:
        pass
    return render(request,"mainpage/blog.html",{'mainblog':mainblog,'single_blog':single_blog,'recent_blog':recent_blog,'instagram_image':instagram_image,'blog_count':blog_count})

def blog_details(request,slug):
    blog_detail = None
    recent_blog = None
    blog_tags = None
    try:
        blog_detail = Blog.objects.get(slug=slug)
    except:
        pass
    try:
        recent_blog = Blog.objects.filter().order_by("-id")[:5]
    except:
        pass
    try:
        blog_tags = Blog.objects.filter(slug=slug).values('keywords')
    except:
        pass
    return render(request,'mainpage/blog_details.html',{'blog_detail':blog_detail,'recent_blog':recent_blog,'blog_tags':blog_tags})

