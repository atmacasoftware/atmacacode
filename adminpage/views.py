from random import randint
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from unidecode import unidecode
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from adminpage.form import TaskForm, NoteForm
from adminpage.models import AdminUser, Task
from blog.models import Blog
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

    return render(request, 'adminpage/signin.html')

def logout(request):
    request.session.clear()
    return redirect('mainpage')

def admin_main_page(request, username):
    user = get_object_or_404(User, username=username)
    if user.is_admin:
        task = Task.objects.filter(authorizedperson=user)
        task_count = task.count()
        return render(request, "adminpage/partials/dashboard.html",
                      {'user': user, 'task': task, 'task_count': task_count})
    return render(request, "adminpage/partials/dashboard.html", {'user': user})

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
                return render(request, "adminpage/partials/add_note.html", {'user': user, 'form': note_form,'task_count':task_count})
            except:
                pass
        return render(request, "adminpage/partials/add_note.html", {'user': user, 'form': note_form,'task_count':task_count})

def blog_page(request,username):
    user = get_object_or_404(User, username=username)
    blog = Blog.objects.filter(user=user)
    task_count = Task.objects.filter(authorizedperson=user).count()
    return render(request,"adminpage/partials/blog_page.html",{'user':user,'blog':blog,'task_count':task_count})