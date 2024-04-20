from blog.models import *
from social_media.models import *

def blog_context(request):
    try:
        recent_blog = Blog.objects.filter().order_by("-id")[:5]
    except:
        recent_blog = Blog.objects.filter().order_by("-id")
    try:
        instagram_image = Instagram.objects.all().order_by("-id")[:6]
    except:
        instagram_image = Instagram.objects.all().order_by("-id")
    return dict(recent_blog=recent_blog,instagram_image=instagram_image)