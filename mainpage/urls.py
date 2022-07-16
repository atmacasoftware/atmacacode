from django.urls import path
from mainpage.views import index,contact
urlpatterns = [
    path('', index, name='mainpage'),
    path('iletisim', contact, name='contact'),
]