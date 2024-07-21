from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from online_users.models import OnlineUserActivity

from adminpage.form import TaskForm, NoteForm
from adminpage.models import Task, BlogCategory, Blog, Education, SiteSettings
from mainpage.models import MainSlider, Subscribe
from student.models import StudentAnnouncements, StudentEducation, StudentQuestions
from user_accounts.models import User
from user_accounts.views import user_count


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
    student_count = User.objects.filter(is_student=True).count()
    customer_count = User.objects.filter(is_customer=True).count()
    user_activity_objects = OnlineUserActivity.get_user_activities()
    number_of_active_users = user_activity_objects.count()

    blog_views = 0

    for b in Blog.objects.all():
        blog_views += b.view_count

    last_ten_blog = Blog.objects.all().order_by('-view_count')[:10]

    return render(request, "backend/pages/mainpage.html",
                  {'user': user, 'student_count': student_count, 'customer_count': customer_count,
                   'number_of_active_users': number_of_active_users, 'blog_views': blog_views,
                   'last_ten_blog': last_ten_blog})


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
            SiteSettings.objects.create(site_name=site_name, site_title=site_title, site_description=site_description,
                                        site_author=site_author, site_keywords=site_keywords, site_logo=site_logo,
                                        site_email=site_email, site_whatsapp=site_whatsapp,
                                        instagram_link=instagram_link, linkedin_link=linkedin_link,
                                        facebook_link=facebook_link, udemy_link=udemy_link)
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
        redirecting_radio = request.POST.get("redirecting_radio")
        redirecting = False
        button_text = request.POST.get("button_text")
        button_url = request.POST.get("button_url")

        if redirecting_radio == 'on':
            redirecting = True

        if slider_title and sub_title and text and image1:
            MainSlider.objects.create(slider_title=slider_title, sub_title=sub_title, content=content, text=text,
                                      image1=image1, image2=image2, details_img=details_img, redirecting=redirecting,
                                      button_text=button_text, button_url=button_url)
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
        button_text = request.POST.get("button_text")
        button_url = request.POST.get("button_url")
        redirecting_radio = request.POST.get("redirecting_radio")
        redirecting = False
        if redirecting_radio == 'on':
            redirecting = True
        slider.slider_title = slider_title
        slider.sub_title = sub_title
        slider.text = text
        slider.content = content
        slider.redirecting=redirecting
        slider.button_url=button_url
        slider.button_text=button_text

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
def view_education_request(request, education_id):
    context = {}
    education = get_object_or_404(Education, id=education_id)
    student_education = StudentEducation.objects.filter(education=education, is_approved=False)

    search = request.GET.get('search')

    if search:
        student_education = student_education.filter(user__first_name__icontains=search)

    p = Paginator(student_education, 30)
    page = request.GET.get('page')
    studenteducation = p.get_page(page)

    context.update({'education': education, 'paginating': studenteducation})

    return render(request, 'backend/pages/education/view_education_request.html', context)


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def view_education_request_approved(request):
    student_id = request.GET.get('student_id')
    education_id = request.GET.get('education_id')
    user_id = request.GET.get('user_id')
    status = request.GET.get('status')

    user = get_object_or_404(User, id=int(user_id))
    education = get_object_or_404(Education, id=int(education_id))
    student_education = StudentEducation.objects.get(user=user, education=education)

    if status == "True" or status == True:
        student_education.is_approved = True
    else:
        student_education.is_approved = False
    student_education.save()
    return JsonResponse(data="success", safe=False)


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


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def users(request):
    context = {}

    search = request.GET.get('search')
    users = User.objects.all()

    if search:
        users = users.filter(Q(first_name__icontains=search) or Q(last_name__icontains=search))

    p = Paginator(users, 30)
    page = request.GET.get('page')
    all_users = p.get_page(page)

    context.update({'paginating': all_users, 'user_count': user_count(request)})

    return render(request, 'backend/pages/users/users.html', context)


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def users_student(request):
    context = {}

    search = request.GET.get('search')
    users = User.objects.filter(is_student=True)

    if search:
        users = users.filter(Q(first_name__icontains=search) or Q(last_name__icontains=search))

    p = Paginator(users, 30)
    page = request.GET.get('page')
    all_users = p.get_page(page)

    context.update({'paginating': all_users, 'user_count': user_count(request)})

    return render(request, 'backend/pages/users/users.html', context)


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def users_customer(request):
    context = {}

    search = request.GET.get('search')
    users = User.objects.filter(is_customer=True)

    if search:
        users = users.filter(Q(first_name__icontains=search) or Q(last_name__icontains=search))

    p = Paginator(users, 30)
    page = request.GET.get('page')
    all_users = p.get_page(page)

    context.update({'paginating': all_users, 'user_count': user_count(request)})

    return render(request, 'backend/pages/users/users.html', context)


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def users_admin(request):
    context = {}

    search = request.GET.get('search')
    users = User.objects.filter(is_superuser=True)

    if search:
        users = users.filter(Q(first_name__icontains=search) or Q(last_name__icontains=search))

    p = Paginator(users, 30)
    page = request.GET.get('page')
    all_users = p.get_page(page)

    context.update({'paginating': all_users, 'user_count': user_count(request)})

    return render(request, 'backend/pages/users/users.html', context)


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def profile(request):
    context = {}
    try:
        subscribe = Subscribe.objects.get(email=request.user.email)
    except:
        subscribe = None

    education_count = StudentEducation.objects.filter(user=request.user).count()
    question_count = StudentQuestions.objects.filter(user=request.user).count()

    context.update({'subscribe': subscribe, 'education_count': education_count, 'question_count': question_count})

    if 'submit' in request.POST:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        mobile = request.POST.get("mobile")
        birthday = request.POST.get("birthday")
        job = request.POST.get("job")
        linkedin = request.POST.get("linkedin")
        github = request.POST.get("github")
        bio = request.POST.get("bio")
        form_subscribe = request.POST.get("subscribe")

        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.mobile = mobile
        if birthday:
            request.user.birthday = birthday
        request.user.job_title = job
        request.user.linkedin = linkedin
        request.user.github = github
        request.user.bio = bio
        request.user.save()

        if form_subscribe == "on":
            if subscribe is None:
                Subscribe.objects.create(email=request.user.email)
        else:
            if subscribe is not None:
                subscribe.delete()

        messages.success(request, 'Hesap başarıyla güncellendi!')
        return redirect('admin_profile')

    return render(request, 'backend/pages/profile/account.html', context)
