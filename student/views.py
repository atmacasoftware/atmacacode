from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from adminpage.models import Education
from announcement.models import Announcement
from mainpage.models import Subscribe
from student.models import *


@login_required(login_url="/giris")
def dashboard(request):
    context = {}
    all_educations = Education.objects.all()
    all_announcements = StudentAnnouncements.objects.all()[:10]
    student_education = StudentEducation.objects.filter(user=request.user)

    if 'newEducationAdd' in request.POST:
        education_id = request.POST.get('select_education')
        email = request.POST.get('select_email')
        if education_id and email:
            education = get_object_or_404(Education, id=int(education_id))

            if StudentEducation.objects.filter(user=request.user, education=education).exists():
                messages.warning(request,'İlgili eğitim zaten eklidir.')
                return redirect('student_dashboard')
            StudentEducation.objects.create(user=request.user,education=education, email=email)
            messages.success(request,
                             'Eğitim eklendi. Admin kontrolü sonrasında panelinizde eğitiminizi görebilirsiniz.')
            return redirect('student_dashboard')

    if 'addQuestion' in request.POST:
        education = request.POST.get('education')
        title = request.POST.get('title')
        content = request.POST.get('content')

        if education is None:
            messages.warning(request, "Eğitim seçmeniz gerekmektedir.")
            return redirect('student_dashboard')

        selectEducation = get_object_or_404(Education, id=int(education))

        if title and content:
            StudentQuestions.objects.create(title=title, content=content, education=selectEducation, user=request.user)
            Announcement.objects.create(users=request.user, title=title, content=content, importance=1, type_choices="Soru")
            messages.success(request, "Sorunuz başarıyla iletildi. 24 saat içerisinde sorunuz cevaplanacaktır.")
            return redirect('student_dashboard')

    context.update({'all_educations': all_educations, 'all_announcements': all_announcements,
                    'student_education': student_education})
    return render(request, 'studentpage/pages/dashboard.html', context)

@login_required(login_url="/giris")
def profile(request):
    context = {}
    try:
        subscribe = Subscribe.objects.get(email=request.user.email)
    except:
        subscribe = None

    education_count = StudentEducation.objects.filter(user=request.user).count()
    question_count = StudentQuestions.objects.filter(user=request.user).count()

    context.update({'subscribe': subscribe, 'education_count':education_count, 'question_count':question_count})

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

    return render(request, 'studentpage/pages/profile/account.html', context)