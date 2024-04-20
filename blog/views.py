from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from blog.form import ReviewForm
from blog.models import Blog,ReviewRating
# Create your views here.
from customers.models import Customer
from social_media.models import Instagram
from user_accounts.models import User


def blog_page(request):
    mainblog = None
    single_blog = None
    blog_count = None
    paged_blog = None
    try:
        mainblog = Blog.objects.filter(is_main_slider=True)[:10]
        paginator = Paginator(mainblog, 10)
        page = request.GET.get('page')
        paged_blog = paginator.get_page(page)
    except:
        pass
    try:
        single_blog = Blog.objects.filter()[:10]
    except:
        pass
    try:
        blog_count = Blog.objects.all().count()
    except:
        pass
    return render(request,"mainpage/blog.html",{'mainblog':mainblog,'single_blog':single_blog,'blog_count':blog_count,'paged_blog':paged_blog})

def blog_details(request,slug):
    blog_detail = None
    blog_tags = None
    previous_post = None
    next_post = None
    review = None
    review_count = None
    try:
        blog_detail = Blog.objects.get(slug=slug)
        next_post = Blog.objects.filter(id=blog_detail.id + 1)
        previous_post = Blog.objects.filter(id=blog_detail.id - 1)
    except:
        pass
    try:
        blog_tags = Blog.objects.filter(slug=slug).values('keywords')
    except:
        pass
    try:
        previous_post = Blog.objects.filter(id=blog_detail.id-1)
    except:
        pass
    try:
        next_post = Blog.objects.filter(id=blog_detail.id+1)
    except:
        pass
    try:
        review = ReviewRating.objects.filter(blog=blog_detail)
        review_count = ReviewRating.objects.filter(blog=blog_detail).count()
    except:
        pass
    return render(request,'mainpage/blog_details.html',{'blog_detail':blog_detail,'blog_tags':blog_tags,'next_post':next_post,'previous_post':previous_post,'review':review,'review_count':review_count})


def submit_review(request, username, blog_id):
    user = get_object_or_404(User,username=username)
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            customer = Customer.objects.get(user=user)
            reviews = ReviewRating.objects.get(customer=customer, blog__id=blog_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            customer = Customer.objects.get(user=user)
            if form.is_valid():
                data = ReviewRating()
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.blog_id = blog_id
                data.customer = customer
                data.save()
                return redirect(url)


def category_details(request, slug):
    blog = None
    message = None
    blog_count = 0
    try:
        blog = Blog.objects.filter(category_slug=slug)
        blog_count = blog.count()
    except:
        message = "Bu kategoride henüz blog yazısı bulunmamaktadır."

    return render(request, "mainpage/category_details.html",{'blog':blog,'message':message,'blog_count':blog_count})

def search(request):
    context = {}
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            blog = Blog.objects.order_by('-created_at').filter(
                Q(content__icontains=keyword) | Q(keywords__icontains=keyword) | Q(title__icontains=keyword))
            blog_count = blog.count()

            context = {
                'blog': blog,
                'blog_count': blog_count,
                'keyword': keyword,
            }
    return render(request, 'mainpage/partials/search_blog_page.html', context)

def blog_tags(request, keyword):
    blog = None
    message = None
    blog_count = 0
    try:
        blog = Blog.objects.filter(keywords=keyword)
        blog_count = blog.count()
    except:
        message = "Bu kategoride henüz blog yazısı bulunmamaktadır."

    return render(request, "mainpage/partials/tags_blog_page.html",{'blog':blog,'message':message,'blog_count':blog_count})