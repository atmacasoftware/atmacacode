from django.urls import path
from mainpage.views import index,contact,details,about_page,conditions,privacy,cookies,kvkk,member_contract
urlpatterns = [
    path('', index, name='mainpage'),
    path('iletisim', contact, name='contact'),
    path('<slug:slug>', details, name='slider_details'),
    path('atmacacode/hakkinda', about_page, name='about_page'),
    path('atmacacode/uyelik-sozlesmesi', member_contract, name='member_contract'),
    path('atmacacode/site-kullanim-sartlari', conditions, name='conditions'),
    path('atmacacode/gizlilik-politikasi', privacy, name='privacy'),
    path('atmacacode/cerezler', cookies, name='cookies'),
    path('atmacacode/kvkk-aydinlatma-metni', kvkk, name='kvkk'),
]