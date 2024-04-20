from django.urls import path
from chat.views import *

urlpatterns = [
    path('<username>', main_chat, name="main-chat"),
    path('mesajlasma/<username>', chatroom, name="chatroom"),
    path('ajax/<username>/', ajax_load_messages, name="chatroom-ajax"),
]