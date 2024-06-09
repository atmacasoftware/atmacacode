from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from adminpage.models import Education
from announcement.models import Announcement
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
