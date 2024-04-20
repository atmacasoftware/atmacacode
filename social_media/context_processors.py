from social_media.models import *

def social_share(request):
    try:
        instagram = Instagram.objects.all()[:6]
    except:
        instagram = Instagram.objects.all()
    return dict(instagram=instagram)