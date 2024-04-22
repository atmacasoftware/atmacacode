from random import randint
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from unidecode import unidecode
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

import blog
from adminpage.form import TaskForm, NoteForm
from adminpage.models import AdminUser, Task, BlogCategory, Blog
from user_accounts.models import User


def admin_login(request):
    try:
        if request.user.is_authenticated:
            messages.success(request, 'Giriş yapıldı')
            return redirect('mainpage')
        if 'loginBtn' in request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')
            remember = request.POST.get('remember_me')
            user_obj = User.objects.filter(email=email)
            if not user_obj.exists():
                messages.error(request, 'Bu kullanıcı mevcut değil.')
                return redirect('admin_login')
            user_obj = authenticate(email=email, password=password)
            if user_obj is not None:
                if User.objects.get(email=email, is_superuser=True):
                    auth_login(request, user_obj)
                    if not remember:
                        request.session.set_expiry(18000)
                    messages.success(request,
                                     f'Hoşgeldin {request.user.get_full_name()}.')
                    return redirect('admin_mainpage')
    except Exception as e:
        return redirect('admin_login')

    return render(request, 'backend/pages/account/login.html')


def logout(request):
    request.session.clear()
    return redirect('mainpage')


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def admin_main_page(request):
    user = request.user
    task = Task.objects.filter(user=user)
    task_count = task.count()
    return render(request, "backend/pages/mainpage.html",
                  {'user': user, 'task': task, 'task_count': task_count})


def calender_page(request):
    return render(request, "adminpage/partials/calendar.html")


def add_task(request, username):
    user = get_object_or_404(User, username=username)
    if user.is_admin:
        tasks_form = TaskForm(data=request.POST or None, files=request.FILES or None)
        if request.method == 'POST':
            try:
                tasks_form = TaskForm(data=request.POST or None, files=request.FILES or None)
                if tasks_form.is_valid():
                    a = tasks_form.save(commit=False)
                    a.authorizedperson = user
                    a.save()
                    messages.add_message(request, messages.SUCCESS, 'Adres Eklendi')
                    return redirect('admin_main_page', user)
                return render(request, "adminpage/partials/add_task.html", {'user': user, 'form': tasks_form})
            except:
                pass
        return render(request, "adminpage/partials/add_task.html", {'user': user, 'form': tasks_form})


def task_page(request, username):
    user = get_object_or_404(User, username=username)
    task = Task.objects.filter(authorizedperson=user)
    task_count = task.count()
    return render(request, "adminpage/partials/task_page.html", {'user': user, 'task': task, 'task_count': task_count})


def task_detail_page(request, username, task_id):
    user = get_object_or_404(User, username=username)
    task = Task.objects.get(authorizedperson=user, task_id=task_id)
    task_count = Task.objects.filter(authorizedperson=user).count()
    return render(request, "adminpage/partials/task_detail.html",
                  {'user': user, 'task': task, 'task_count': task_count})


def add_note_page(request, username):
    user = get_object_or_404(User, username=username)
    task_count = Task.objects.filter(authorizedperson=user).count()
    if user.is_admin:
        note_form = NoteForm(data=request.POST or None, files=request.FILES or None)
        if request.method == 'POST':
            try:
                note_form = NoteForm(data=request.POST or None, files=request.FILES or None)
                if note_form.is_valid():
                    a = note_form.save(commit=False)
                    a.authorizedperson = user
                    a.save()
                    messages.add_message(request, messages.SUCCESS, 'Adres Eklendi')
                    return redirect('admin_main_page', user)
                return render(request, "adminpage/partials/add_note.html",
                              {'user': user, 'form': note_form, 'task_count': task_count})
            except:
                pass
        return render(request, "adminpage/partials/add_note.html",
                      {'user': user, 'form': note_form, 'task_count': task_count})


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def blog_all(request):
    context = {}
    blogs = Blog.objects.select_related('user').all()
    context.update({'blogs': blogs})
    return render(request, "backend/pages/blog/all.html", context)


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def blog_view_and_update(request, id):
    context = {}
    blog = get_object_or_404(Blog, id=id)
    blog_category = BlogCategory.objects.select_related().all()

    if 'saveBtn' in request.POST:
        name = request.POST.get("name")
        category = request.POST.get("category")
        content = request.POST.get("content")
        status = request.POST.get("status")
        image = request.FILES.get("image")

        blog_category = get_object_or_404(BlogCategory, id=int(category))
        blog.name = name
        blog.category = blog_category
        blog.text = content
        blog.status = status
        blog.image = image
        blog.save()

        messages.add_message(request, messages.SUCCESS, "Blog yazısı başarıyla güncellendi.")
        return redirect('blog_view_and_update', id)

    context.update({'blog': blog, 'blog_category': blog_category})
    return render(request, "backend/pages/blog/update.html", context)


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def blog_yeni_yazi(request):
    context = {}
    user = request.user
    blog_category = BlogCategory.objects.select_related().all()

    if 'saveBtn' in request.POST:
        name = request.POST.get("name")
        category = request.POST.get("category")
        content = request.POST.get("content")
        status = request.POST.get("status")
        image = request.FILES.get("image")

        blog_category = get_object_or_404(BlogCategory, id=int(category))

        Blog.objects.create(user=request.user, name=name, category=blog_category, text=content, status=status,
                            image=image)
        messages.add_message(request, messages.SUCCESS, "Blog yazısı başarıyla eklendi.")
        return redirect('blog_yeni_yazi')

    context.update({'blog_category': blog_category})
    return render(request, "backend/pages/blog/new.html", context)


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def blog_category(request):
    context = {}
    blog_category = BlogCategory.objects.select_related().all()

    if 'saveBtn' in request.POST:
        name = request.POST.get('name')
        if name:
            BlogCategory.objects.create(name=name)
            messages.add_message(request, messages.SUCCESS, 'Kategori eklendi.')
            return redirect('blog_category')
        messages.add_message(request, messages.ERROR, 'Bir hata meydana geldi.')
        return redirect('blog_category')

    context.update({'blog_category': blog_category})

    return render(request, "backend/pages/blog/kategori.html", context)


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def blog_category_delete(request, id):
    blog_category = get_object_or_404(BlogCategory, id=id)
    blog_category.delete()
    messages.add_message(request, messages.SUCCESS, 'Kategori silindi.')
    return redirect('blog_category')


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def blog_change_status(request, id, stat):
    blog = get_object_or_404(Blog, id=id)
    if blog.status == "Yayınla":
        if stat == "taslak":
            blog.status = "Taslak"
        elif stat == "aski":
            blog.status = "Askıya Al"
    elif blog.status == "Taslak":
        if stat == "yayinla":
            blog.status = "Yayınla"
        elif stat == "aski":
            blog.status = "Askıya Al"
    elif blog.status == "Askıya Al":
        if stat == "yayinla":
            blog.status = "Yayınla"
        elif stat == "taslak":
            blog.status = "Taslak"
    blog.save()
    return redirect("blog_all")

@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def blog_delete(request, id):
    blog = get_object_or_404(Blog, id=id)
    blog.delete()
    return redirect("blog_all")