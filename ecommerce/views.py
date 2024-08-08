from django.contrib import messages
from django.shortcuts import render, redirect
from ecommerce.models import *


# Create your views here.

def customers(request):
    context = {}
    customer = Customer.objects.all()
    s_type = SubscriptionType.objects.all()
    context.update({'customer': customer, 's_type':s_type})

    if 'submitBtn' in request.POST:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        mobile =request.POST['mobile']
        subscription_type = request.POST['subscription_type']

        if first_name and last_name and email and mobile and subscription_type:
            subscription = SubscriptionType.objects.get(id=subscription_type)
            Customer.objects.create(first_name=first_name, last_name=last_name, email=email, mobile=mobile, subscription_type=subscription)
            messages.success(request, 'Müşteri başarıyla eklendi !')
            return redirect("ecommerce_customer")
    return render(request, 'backend/pages/entegration/customer.html', context)

def subscription(request):
    context = {}
    subscription = SubscriptionType.objects.all()
    context.update({'subscription': subscription})

    if 'submitBtn' in request.POST:
        subscription_name = request.POST['subscription_name']
        duration = request.POST['duration']

        if subscription_name and duration:
            SubscriptionType.objects.create(name=subscription_name, duration=duration)
            messages.success(request, 'Abonelik tipi başarıyla eklendi !')
            return redirect("ecommerce_subscription")
    return render(request, 'backend/pages/entegration/subscription_type.html', context)

def marketplace(request):
    context = {}
    marketplace = MarketPlaces.objects.all()
    context.update({'marketplace': marketplace})

    if 'submitBtn' in request.POST:
        name = request.POST['name']

        if name:
            MarketPlaces.objects.create(name=name)
            messages.success(request, 'Pazaryeri başarıyla eklendi !')
            return redirect("ecommerce_marketplace")
    return render(request, 'backend/pages/entegration/marketplaces.html', context)

def supported_type(request):
    context = {}
    supported = SupportedTypes.objects.all()
    context.update({'supported': supported})

    if 'submitBtn' in request.POST:
        name = request.POST['name']
        image = request.FILES.get('image')

        if name and image:
            SupportedTypes.objects.create(name=name, image=image)
            messages.success(request, 'Desteklenen XML tipi başarıyla eklendi !')
            return redirect("ecommerce_supported_type")
    return render(request, 'backend/pages/entegration/supported_types.html', context)