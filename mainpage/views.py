from django.shortcuts import render, redirect

from blog.models import Blog
from mainpage.forms import ContactForm, SubscribeForm
from products.models import Services
from user_accounts.models import Account
# Create your views here.

def index(request):
    blog = None
    services = None
    try:
        blog = Blog.objects.all()[:3]
    except:
        pass
    try:
        services = Services.objects.all()
    except:
        pass
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "mainpage/mainpage.html", {'blog': blog, 'services': services})
    return render(request, "mainpage/mainpage.html",{'blog':blog,'services':services})


def contact(request):
    status = ""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            status = "Mesajınız gönderildi. En kısa sürede sizinle iletişime geçilecektir."
            return render(request, "mainpage/contact.html",{'status':status})
        return render(request, "mainpage/contact.html")
    return render(request, "mainpage/contact.html")


