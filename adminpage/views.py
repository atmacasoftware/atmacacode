from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from adminpage.form import TaskForm, NoteForm
from adminpage.models import Task, BlogCategory, Blog, Education, SiteSettings
from mainpage.models import MainSlider
from student.models import StudentAnnouncements
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


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def general_settings(request):
    context = {}

    site = SiteSettings.objects.all().last()

    context.update({'setting': site})

    if 'submit' in request.POST:
        site_name = request.POST.get("site_name")
        site_title = request.POST.get("site_title")
        site_description = request.POST.get("site_description")
        site_author = request.POST.get("site_author")
        site_keywords = request.POST.get("site_keywords")
        site_logo = request.FILES.get("site_logo")
        site_email = request.POST.get("site_email")
        site_whatsapp = request.POST.get("site_whatsapp")
        instagram_link = request.POST.get("instagram_link")
        linkedin_link = request.POST.get("linkedin_link")
        facebook_link = request.POST.get("facebook_link")
        youtube_link = request.POST.get("youtube_link")
        udemy_link = request.POST.get("udemy_link")

        if site:
            site.site_name = site_name
            site.site_title = site_title
            site.site_description = site_description
            site.site_author = site_author
            site.site_keywords = site_keywords
            site.site_logo = site_logo
            site.site_email = site_email
            site.site_whatsapp = site_whatsapp
            site.instagram_link = instagram_link
            site.linkedin_link = linkedin_link
            site.facebook_link = facebook_link
            site.youtube_link = youtube_link
            site.udemy_link = udemy_link
            site.save()
            messages.success(request, "Site ayarları güncellendi!")
            return redirect('general_settings')

        if site is None:
            SiteSettings.objects.create(site_name=site_name, site_title=site_title, site_description=site_description, site_author=site_author, site_keywords=site_keywords, site_logo=site_logo, site_email=site_email, site_whatsapp=site_whatsapp, instagram_link=instagram_link, linkedin_link=linkedin_link, facebook_link=facebook_link, udemy_link=udemy_link)
            messages.success(request, "Site ayarları oluşturuldu!")
        messages.error(request, "Bir hata meydana geldi!")
        return redirect('general_settings')

    return render(request, 'backend/pages/management/site-settings.html', context)


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
def general_announcement(request):
    context = {}

    mainsliders = MainSlider.objects.all()

    p = Paginator(mainsliders, 10)
    page = request.GET.get('page')
    mainslider = p.get_page(page)

    context.update({'mainslider': mainslider})

    if 'submit' in request.POST:
        slider_title = request.POST.get("slider_title")
        sub_title = request.POST.get("sub_title")
        text = request.POST.get("text")
        content = request.POST.get("content")
        image1 = request.FILES.get("image1")
        image2 = request.FILES.get("image2")
        details_img = request.FILES.get("details_img")

        if slider_title and sub_title and text and content and image1 and details_img:
            MainSlider.objects.create(slider_title=slider_title, sub_title=sub_title, text=text, content=content,
                                      image1=image1, image2=image2, details_img=details_img)
            messages.success(request, "Duyuru eklendi!")
            return redirect('general_announcement')
        messages.error(request, "Bir hata meydana geldi!")
        return redirect('general_announcement')

    return render(request, 'backend/pages/management/announcement.html', context)


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def announcement_all_delete(request):
    sliders = MainSlider.objects.all()
    for s in sliders:
        s.delete()
    messages.success(request, "Tüm duyurular silindi!")
    return redirect('general_announcement')


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def announcement_delete(request, id):
    slider = get_object_or_404(MainSlider, id=id)
    slider.delete()
    messages.success(request, "İlgili duyuru silindi!")
    return redirect('general_announcement')


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def announcement_update(request, id):
    slider = get_object_or_404(MainSlider, id=id)
    if 'submit' in request.POST:
        slider_title = request.POST.get("slider_title")
        sub_title = request.POST.get("sub_title")
        text = request.POST.get("text")
        content = request.POST.get("content")
        image1 = request.FILES.get("image1")
        image2 = request.FILES.get("image2")
        details_img = request.FILES.get("details_img")
        slider.slider_title = slider_title
        slider.sub_title = sub_title
        slider.text = text
        slider.content = content

        if image1:
            slider.image1 = image1
        if image2:
            slider.image2 = image2
        if details_img:
            slider.details_img = details_img

        slider.save()
        messages.success(request, "Duyuru güncellendi!")
        return redirect('announcement_update', id)
    return render(request, 'backend/pages/management/announcement-update.html', context={'slider': slider})


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
        description = request.POST.get("description")
        category = request.POST.get("category")
        content = request.POST.get("content")
        status = request.POST.get("status")
        image = request.FILES.get("image")

        blog_category = get_object_or_404(BlogCategory, id=int(category))
        blog.name = name
        blog.description = description
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
        description = request.POST.get("description")
        category = request.POST.get("category")
        content = request.POST.get("content")
        status = request.POST.get("status")
        image = request.FILES.get("image")

        blog_category = get_object_or_404(BlogCategory, id=int(category))

        Blog.objects.create(user=request.user, name=name, description=description, category=blog_category, text=content,
                            status=status,
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


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def education(request):
    context = {}
    educations = Education.objects.all()
    context.update({'educations': educations})
    if 'submit' in request.POST:
        name = request.POST.get("education_name")
        if not Education.objects.filter(name=name).exists():
            Education.objects.create(name=name, status=True)
            return redirect('education')
    return render(request, 'backend/pages/education/education.html', context)


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def student_announcement(request):
    context = {}
    announcement = StudentAnnouncements.objects.all()

    p = Paginator(announcement, 50)
    page = request.GET.get('page')
    announcements = p.get_page(page)

    context.update({'announcement': announcements})
    if 'submit' in request.POST:
        title = request.POST.get("title")
        content = request.POST.get("content")
        StudentAnnouncements.objects.create(title=title, text=content)
        return redirect('student_announcement')

    return render(request, 'backend/pages/education/announcement.html', context)


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def student_announcement_delete(request, id):
    announcement = get_object_or_404(StudentAnnouncements, id=id)
    announcement.delete()
    messages.success(request, 'İlgili duyuru silindi!')
    return redirect('student_announcement')


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def student_announcement_delete_all(request):
    announcement = StudentAnnouncements.objects.all()
    for a in announcement:
        a.delete()
    messages.success(request, 'Tüm duyurular silindi!')
    return redirect('student_announcement')


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def student_announcement_showing(request, id):
    context = {}
    announcement = get_object_or_404(StudentAnnouncements, id=id)

    context.update({'announcement': announcement})
    return render(request, 'backend/pages/education/announcement_show.html', context)
