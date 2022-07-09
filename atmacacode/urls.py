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
from django.urls import path, re_path, include
from django.views.generic import RedirectView
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainpage.urls')),
    path('blog', include('blog.urls')),
    path('hizmetler', include('products.urls')),
    path('yonetim-paneli/', include('adminpage.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('favicon.ico', RedirectView.as_view(url='/static/img/logo/small_logo.png')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

admin.site.site_title = 'Atmaca Code Yönetimi'
admin.site.site_header = 'Atmaca Code Yönetimi Paneli'
admin.site.index_title = 'Atmaca Code Yönetimi Paneline Hoş Geldiniz'
