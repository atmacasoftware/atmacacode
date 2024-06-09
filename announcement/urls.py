from django.urls import path
from announcement.views import *


urlpatterns = [
    path("bildirim-yenile",refresh_bildirim, name="refresh_bildirim"),
    path("tum-bildirimler",all_announcements, name="all_announcements"),
    path("tumunu-okundu-olarak-isaretle",all_read_announcement, name="all_read_announcement"),
    path("tum-bildirimler-sil",all_delete_announcement, name="all_delete_announcement"),
    path("bildirim/sil/<int:id>",delete_announcement, name="delete_announcement"),
    path("bildirim/goruntule/<int:id>",show_announcement, name="show_announcement"),
]