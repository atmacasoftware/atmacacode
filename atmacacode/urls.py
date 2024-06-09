"""atmacacode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, re_path, include
from django.views.generic import RedirectView
from django.views.static import serve
from django.conf import settings
from django.contrib.auth import views as auth_views

from site_map.views import RobotsTxtView
from site_map.sitemaps import *

sitemaps = {
    'products': ProductMap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainpage.urls')),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}),
    path('robots.txt/', RobotsTxtView.as_view()),
    path('hesap/', include('customers.urls')),
    path('bildirim-servisi/', include('announcement.urls')),
    path('ogrenci/', include('student.urls')),
    path('hizmetler', include('products.urls')),
    path('', include('adminpage.urls')),
    path('mesajlasma/', include('chat.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),

    path('favicon.ico', RedirectView.as_view(url='/static/img/logo/small_logo.png')),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="backend/pages/account/forgot_password.html"),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="backend/pages/account/password_reset_send.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="backend/pages/account/set_password.html"),
         name="password_reset_confirm"),
    path('reset_password_complate/',
         auth_views.PasswordResetCompleteView.as_view(template_name="backend/pages/account/password_reset_complate.html"),
         name="password_reset_complete"),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

admin.site.site_title = 'Atmaca Code'
admin.site.site_header = 'Atmaca Code Yönetimi Paneli'
admin.site.index_title = 'Atmaca Code Yönetimi Paneline Hoş Geldiniz'
