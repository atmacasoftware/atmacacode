from django.urls import path
from adminpage.views import *
from adminpage.api_views import *

urlpatterns = [
    path('yonetim-paneli/', admin_main_page, name="admin_main_page"),
    path('yonetim-paneli/yonetim-paneli-giris/', admin_login, name="admin_login"),
    path('yonetim-paneli/takvim', calender_page, name="calender"),
    path('yonetim-paneli/gorev-ekle/<username>/', add_task, name="add_task"),
    path('yonetim-paneli/cikis-yap/', logout, name="logout"),
    path('yonetim-paneli/gorevler/<username>/', task_page, name="task_page"),
    path('yonetim-paneli/gorev/<int:task_id>/<username>/', task_detail_page, name="task_detail_page"),
    path('yonetim-paneli/not-ekle/<username>/', add_note_page, name="add_note_page"),
    path('yonetim-paneli/site-yonetimi/site-ayarlari/', general_settings, name="general_settings"),
    path('yonetim-paneli/site-yonetimi/duyurular/', general_announcement, name="general_announcement"),
    path('yonetim-paneli/site-yonetimi/duyurular/hepsini-sil', announcement_all_delete, name="announcement_all_delete"),
    path('yonetim-paneli/site-yonetimi/duyurular/sil/<int:id>', announcement_delete, name="announcement_delete"),
    path('yonetim-paneli/site-yonetimi/duyurular/guncelle/<int:id>', announcement_update, name="announcement_update"),
    path('yonetim-paneli/blog/tum-yazilar/', blog_all, name="blog_all"),
    path('yonetim-paneli/blog/tum-yazilar/goruntule-guncelle/id=<int:id>/', blog_view_and_update, name="blog_view_and_update"),
    path('yonetim-paneli/blog/tum-yazilar/durum-degistir/id=<int:id>/durum=<str:stat>/', blog_change_status, name="blog_change_status"),
    path('yonetim-paneli/blog/tum-yazilar/sil/id=<int:id>/', blog_delete, name="blog_delete"),
    path('yonetim-paneli/blog/yeni-yazi-ekle/', blog_yeni_yazi, name="blog_yeni_yazi"),
    path('yonetim-paneli/blog/kategoriler/', blog_category, name="blog_category"),
    path('yonetim-paneli/blog/kategoriler/kategori-sil/id=<int:id>/', blog_category_delete, name="blog_category_delete"),
    path('yonetim-paneli/egitim-yonetimi/', education, name="education"),
    path('yonetim-paneli/egitim-yonetimi/istekler/egitim-id=<int:education_id>/', view_education_request, name="view_education_request"),
    path('yonetim-paneli/egitim-yonetimi/istekler/istek-onayla/', view_education_request_approved, name="view_education_request_approved"),
    path('yonetim-paneli/egitim-yonetimi/duyurular/', student_announcement, name="student_announcement"),
    path('yonetim-paneli/egitim-yonetimi/duyurular/sil/<int:id>/', student_announcement_delete, name="student_announcement_delete"),
    path('yonetim-paneli/egitim-yonetimi/duyurular/hepsini-sil/', student_announcement_delete_all, name="student_announcement_delete_all"),
    path('yonetim-paneli/egitim-yonetimi/duyurular/goruntule/<int:id>/', student_announcement_showing, name="student_announcement_showing"),
    path('yonetim-paneli/hesabim/', profile, name="admin_profile"),
    path('yonetim-paneli/kullanici-yonetimi/tum-kullanicilar/hepsi/', users, name="admin_users"),
    path('yonetim-paneli/kullanici-yonetimi/tum-kullanicilar/ogrenci/', users_student, name="admin_users_student"),
    path('yonetim-paneli/kullanici-yonetimi/tum-kullanicilar/musteri/', users_customer, name="admin_users_customer"),
    path('yonetim-paneli/kullanici-yonetimi/tum-kullanicilar/admin/', users_admin, name="admin_users_admin"),

    ## API
    path('blog/api/tum-yazilar/', BlogApiView.as_view()),
    path('blog/api/tum-yazilar/yazi/<str:slug>/', blog_detail),
    path('blog/api/kategoriler/', BlogCategoryApiView.as_view()),
]
