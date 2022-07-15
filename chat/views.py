from django.shortcuts import render
# Create your views here.
from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.
import json

from chat.models import Message
from customers.models import Customer
from user_accounts.models import Account
from atmacacode.settings import AUTH_USER_MODEL
User = AUTH_USER_MODEL

def main_chat(request, username):
    context = {}
    user = get_object_or_404(Account, username=username)
    if user.is_customer:
        chat_messages = Message.objects.filter(Q(receiver__username=request.user.username)).values("sender").annotate(
            Count('sender_id')).order_by().filter(sender_id__gt=1)
        customer = Customer.objects.get(user=user)
        context.update({'messages': chat_messages})
        contact_list = []
        context.update({'contact_list': contact_list,'user':user,'customer':customer})
        for m in chat_messages:
            user = get_object_or_404(User, id=m.get('sender'))
            contact_list.append(user)
        return render(request, "mainpage/partials/message_list.html", context)
    else:
        return render(request,'error_page.html')

def chatroom(request, username):
    other_user = get_object_or_404(Account, username=username)
    user = get_object_or_404(Account, username=username)
    if user.is_customer:
        customer = Customer.objects.get(authorizedperson=user)
        messages = Message.objects.filter(Q(receiver__username=request.session['username'], sender=other_user))
        messages.update(seen=True)
        messages = messages | Message.objects.filter(Q(receiver=other_user, sender__username=request.session['username']))
        chat_messages = Message.objects.filter(Q(receiver__username=request.session['username'])).values("sender").annotate(
            Count('sender_id')).order_by().filter(sender_id__gt=1)
        contact_list = []
        for m in chat_messages:
            user = get_object_or_404(User, id=m.get('sender'))
            contact_list.append(user)

        return render(request, "mainpage/partials/chatroom.html", {"other_user": other_user, 'contact_list': contact_list, "messages": messages,'user':user,'customer':customer})
    else:
        return render(request,'error_page.html')

def ajax_load_messages(request, username):
    other_user = get_object_or_404(Account, username=username)
    request_user = get_object_or_404(Account, username=request.session['username'])
    messages = Message.objects.filter(seen=False, receiver=request_user)

    message_list = [{
        "sender": message.sender.username,
        "message": message.message,
        "sent": message.sender == request.session['username']
    } for message in messages]
    messages.update(seen=True)
    if request.method == 'POST':
        message = json.loads(request.body)
        m = Message.objects.create(receiver=other_user, sender=request_user, message=message)
        message_list.append({
            "sender": request.user.username,
            "message": m.message,
            "sent": True,
        })
    return JsonResponse(message_list, safe=False)
