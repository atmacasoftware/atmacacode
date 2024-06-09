from announcement.models import Announcement

def not_read_announcement(request):
    if request.user.is_authenticated:
        notify = Announcement.objects.filter(is_read=False)
        notify_count = Announcement.objects.filter(is_read=False).count()
        return dict(notify=notify, notify_count=notify_count)
    else:
        return dict(notify=False)