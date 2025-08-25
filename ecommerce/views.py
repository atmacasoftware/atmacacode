from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from ecommerce.models import *


# Create your views here.
@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
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

@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
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

@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def marketplace(request):
    context = {}
    marketplace = MarketPlaces.objects.all()
    context.update({'marketplace': marketplace})

    if 'submitBtn' in request.POST:
        name = request.POST['name']
        active = request.POST.get('active', None)

        if name:
            if active:
                MarketPlaces.objects.create(name=name, is_active=active)
            else:
                MarketPlaces.objects.create(name=name, is_active=False)
            messages.success(request, 'Pazaryeri başarıyla eklendi !')
            return redirect("ecommerce_marketplace")
    return render(request, 'backend/pages/entegration/marketplaces.html', context)

@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def supported_type(request):
    context = {}
    supported = SupportedTypes.objects.all()
    note = SupportedTypesNotes.objects.all()
    context.update({'supported': supported, 'note':note.last()})

    if 'submitBtn' in request.POST:
        name = request.POST['name']
        image = request.FILES.get('image')

        if name and image:
            SupportedTypes.objects.create(name=name, image=image)
            messages.success(request, 'Desteklenen XML tipi başarıyla eklendi !')
            return redirect("ecommerce_supported_type")

    if 'submitNoteBtn' in request.POST:
        notes = request.POST['notes']
        if notes:
            if note.count() < 1:
                SupportedTypesNotes.objects.create(note=notes)
                messages.success(request, 'Not başarıyla eklendi !')
                return redirect("ecommerce_supported_type")
            else:
                data = note.last()
                data.note = notes
                data.save()
                messages.success(request, 'Not başarıyla güncellendi !')
                return redirect("ecommerce_supported_type")

    return render(request, 'backend/pages/entegration/supported_types.html', context)
@login_required(login_url="/yonetim-paneli/yonetim-paneli-giris/")
def notes(request):
    context = {}
    supported_type_notes = SupportedTypesNotes.objects.all()
    adjusted_prices_notes = AdjustedPriceNotes.objects.all()
    context.update({'supported_type_notes': supported_type_notes.last(), 'adjusted_prices_notes': adjusted_prices_notes.last()})

    if 'submitPriceType' in request.POST:
        notes = request.POST['notes']

        if notes:
            if adjusted_prices_notes.count() < 1:
                AdjustedPriceNotes.objects.create(note=notes)
                messages.success(request, 'Fiyat ayarlama notları başarıyla eklendi !')
                return redirect("ecommerce_notes")
            else:
                data = adjusted_prices_notes.last()
                data.note = notes
                data.save()
                messages.success(request, 'Fiyat ayarlama notları başarıyla güncellendi !')
                return redirect("ecommerce_notes")

    if 'submitSuppertedType' in request.POST:
        notes = request.POST['notes']

        if notes:
            if supported_type_notes.count() < 1:
                SupportedTypesNotes.objects.create(note=notes)
                messages.success(request, 'Desteklenen XML notları başarıyla eklendi !')
                return redirect("ecommerce_notes")
            else:
                data = supported_type_notes.last()
                data.note = notes
                data.save()
                messages.success(request, 'Desteklenen XML notları başarıyla güncellendi !')
                return redirect("ecommerce_notes")

    return render(request, 'backend/pages/entegration/notes.html', context)