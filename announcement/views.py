from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from announcement.models import Announcement


# Create your views here.

def refresh_bildirim(request):
    exists_notification = Announcement.objects.filter(is_read=False).exists()

    notification_list = []

    notification = Announcement.objects.filter(is_read=False)

    for n in notification:
        notification_list.append({
            'id': n.id,
            'n_type': n.type_choices,
            'title': n.title,
            'passing_time': n.passing_time(),
        })

    data = [exists_notification, notification_list]

    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def all_announcements(request):
    context = {}
    announcement = Announcement.objects.all()
    context.update({'announcement': announcement})
    return render(request, '', context)

@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def all_read_announcement(request):
    announcement = Announcement.objects.all()
    for a in announcement:
        a.is_read = True
        a.save()
    data = "success"
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def all_delete_announcement(request):
    announcement = Announcement.objects.all().delete()
    messages.info(request, 'Tüm bildirimler silindi.')
    return redirect('all_announcements')


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def delete_announcement(request, id):
    announcement = get_object_or_404(Announcement, id=id)
    announcement.delete()
    messages.info(request, 'İlgili bildirim silindi.')
    return redirect('all_announcements')


@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def show_announcement(request, id):
    context = {}
    announcement = get_object_or_404(Announcement, id=id)

    context.update({
        'announcement': announcement,
    })

    return render(request, "backend/yonetim/sayfalar/bildirim_oku.html", context)
