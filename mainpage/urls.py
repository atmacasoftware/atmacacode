from django.urls import path
from mainpage.views import index,contact,details
urlpatterns = [
    path('', index, name='mainpage'),
    path('iletisim', contact, name='contact'),
    path('<slug:slug>', details, name='slider_details')
]