from django.shortcuts import render, redirect

from blog.form import ReviewForm
from blog.models import Blog,ReviewRating
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
    previous_post = None
    next_post = None
    try:
        blog_detail = Blog.objects.get(slug=slug)
        next_post = Blog.objects.filter(id=blog_detail.id + 1)
        previous_post = Blog.objects.filter(id=blog_detail.id - 1)
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
    try:
        previous_post = Blog.objects.filter(id=blog_detail.id-1)
        print(previous_post.id)
    except:
        pass
    try:
        next_post = Blog.objects.filter(id=blog_detail.id+1)
        print(next_post.id)
    except:
        pass
    return render(request,'mainpage/blog_details.html',{'blog_detail':blog_detail,'recent_blog':recent_blog,'blog_tags':blog_tags,'next_post':next_post,'previous_post':previous_post})


def submit_review(request, blog_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            customer_id = request.session.get('customer')
            reviews = ReviewRating.objects.get(user__id=customer_id, blog__id=blog_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.blog_id = blog_id
                data.user_id = request.session.get('customer')
                data.save()
                return redirect(url)

