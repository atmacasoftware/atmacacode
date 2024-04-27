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
    path('yonetim-paneli/blog/tum-yazilar/', blog_all, name="blog_all"),
    path('yonetim-paneli/blog/tum-yazilar/goruntule-guncelle/id=<int:id>/', blog_view_and_update, name="blog_view_and_update"),
    path('yonetim-paneli/blog/tum-yazilar/durum-degistir/id=<int:id>/durum=<str:stat>/', blog_change_status, name="blog_change_status"),
    path('yonetim-paneli/blog/tum-yazilar/sil/id=<int:id>/', blog_delete, name="blog_delete"),
    path('yonetim-paneli/blog/yeni-yazi-ekle/', blog_yeni_yazi, name="blog_yeni_yazi"),
    path('yonetim-paneli/blog/kategoriler/', blog_category, name="blog_category"),
    path('yonetim-paneli/blog/kategoriler/kategori-sil/id=<int:id>/', blog_category_delete, name="blog_category_delete"),


    ## API
    path('blog/api/tum-yazilar/', BlogApiView.as_view()),
    path('blog/api/tum-yazilar/yazi/<str:slug>/', blog_detail),
    path('blog/api/kategoriler/', BlogCategoryApiView.as_view()),
]
