from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from announcement.models import Announcement
from customers.forms import CustomerProfileUpdateForm
from customers.models import Customer, WhyDelete
from order.models import Order
from supports.models import SupportRoom, Support, AnswerSupport
from user_accounts.models import User


def register(request):
    try:
        if request.user.is_authenticated:
            messages.success(request, 'Giriş yapıldı')
            return redirect('mainpage')
        if 'business-signup' in request.POST:
            first_name = request.POST.get('b-firstname')
            last_name = request.POST.get('b-lastname')
            email = request.POST.get('b-email')
            mobile = request.POST.get('b-phone')
            password = request.POST.get('b-password1')
            user_obj = User.objects.filter(email=email)
            if user_obj.exists():
                messages.warning(request, 'Bu kullanıcı zaten mevcuttur!')
                return redirect('customer_login')
            hass_pass = make_password(password)
            User.objects.create(first_name=first_name, last_name=last_name, email=email, mobile=mobile,
                                password=hass_pass, is_contract=True, is_customer=True)
            return redirect('customer_login')
        if 'education-signup' in request.POST:
            first_name = request.POST.get('e-firstname')
            last_name = request.POST.get('e-lastname')
            email = request.POST.get('e-email')
            password = request.POST.get('e-password1')
            user_obj = User.objects.filter(email=email)
            if user_obj.exists():
                messages.warning(request, 'Bu kullanıcı zaten mevcuttur!')
                return redirect('customer_login')
            hass_pass = make_password(password)
            User.objects.create(first_name=first_name, last_name=last_name, email=email,
                                password=hass_pass, is_contract=True, is_student=True)
            return redirect('customer_login')
        return render(request, 'mainpage/register.html')
    except Exception as e:
        messages.error(request, 'Bir hata meydana geldi!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def customer_login(request):
    try:
        if request.user.is_authenticated:
            messages.success(request, 'Giriş yapıldı')
            return redirect('mainpage')
        if 'login-btn' in request.POST:
            email = request.POST.get("email")
            password = request.POST.get("password")
            user_obj = User.objects.filter(email=email)
            if not user_obj.exists():
                messages.warning(request, 'Bu kullanıcı mevcut değildir!')
                return redirect('customer_login')
            user_obj = authenticate(email=email, password=password)
            if user_obj is not None:
                if User.objects.get(email=email, is_student=True):
                    auth_login(request, user_obj)
                    return redirect('student_dashboard')
                messages.warning(request, 'Bir hata meydana geldi!')
                return redirect('customer_login')
        return render(request, 'mainpage/login.html')
    except:
        messages.warning(request, 'Bir hata meydana geldi!')
        return redirect('customer_login')


@login_required
def logout(request):
    request.session.clear()
    return redirect('mainpage')


@login_required
def profile_page(request, username):
    user = get_object_or_404(User, username=username)
    if user.is_customer:
        customer = Customer.objects.get(user=user)
        announcement_count = Announcement.objects.filter(users=user, is_active=True).count()
        update_form = CustomerProfileUpdateForm(instance=customer, data=request.POST or None,
                                                files=request.FILES or None)
        try:
            update_form = CustomerProfileUpdateForm(instance=customer, data=request.POST or None,
                                                    files=request.FILES or None)
            if 'update_profile' in request.POST:
                if update_form.is_valid():
                    update_form.save(commit=True)
                    return render(request, "mainpage/customer_edit.html",
                                  {'customer': customer, 'update_form': update_form,
                                   'announcement_count': announcement_count})

                else:
                    return render(request, "mainpage/customer_edit.html",
                                  {'customer': customer, 'update_form': update_form,
                                   'announcement_count': announcement_count})
            elif 'change_password' in request.POST:
                postData = request.POST
                password = postData.get('password')
                haspass = make_password(password)
                cust = customer
                user.password = haspass
                user.save()

                cust.password = password
                cust.password = make_password(cust.password)
                cust.save()
                messages.add_message(request, messages.SUCCESS, 'Şifre başarıyla güncellendi.')
                return redirect("customer_login")

            elif 'delete_account' in request.POST:
                postData = request.POST
                password = postData.get('current-password')
                if password != '':
                    flag = check_password(password, user.password)
                    if flag:
                        delete_account = WhyDelete.objects.create()
                        delete_account.email = customer.email
                        reason = postData.get('reason')
                        if reason != '':
                            delete_account.reason = reason
                            delete_account.save()
                            user.delete()
                            customer.delete()
                            return redirect("mainpage")
                        else:
                            delete_error = "Silme nedeniniz boş bırakılamaz!"
                            return render(request, "mainpage/customer_edit.html",
                                          {'customer': customer, 'update_form': update_form,
                                           'delete_error': delete_error, 'announcement_count': announcement_count})

                else:
                    delete_error = "Mevcut şifre boş bırakılamaz!"
                    return render(request, "mainpage/customer_edit.html",
                                  {'customer': customer, 'update_form': update_form, 'delete_error': delete_error,
                                   'announcement_count': announcement_count})
            elif 'is_subscribe' in request.POST:
                postData = request.POST
                is_checked = postData.get('subscribe')
                if is_checked == 'on':
                    customer.is_subscribe = True
                    customer.save()
                else:
                    customer.is_subscribe = False
                    customer.save()

                return render(request, "mainpage/customer_edit.html",
                              {'customer': customer, 'update_form': update_form,
                               'announcement_count': announcement_count})
            else:
                return render(request, "mainpage/customer_edit.html",
                              {'customer': customer, 'update_form': update_form,
                               'announcement_count': announcement_count})
        except:
            pass
        return render(request, "mainpage/customer_edit.html",
                      {'customer': customer, 'update_form': update_form, 'announcement_count': announcement_count})
    else:
        redirect("mainpage")


def order_page(request, username):
    user = get_object_or_404(User, username=username)
    if user.is_customer:
        customer = Customer.objects.get(user=user)
        orders = Order.objects.filter(customer=customer)
        announcement_count = Announcement.objects.filter(users=user, is_active=True).count()
        return render(request, "mainpage/order_page.html",
                      {'customer': customer, 'orders': orders, 'announcement_count': announcement_count})


def announcement_page(request, username):
    user = get_object_or_404(User, username=username)
    if user.is_customer:
        customer = Customer.objects.get(user=user)
        announcement = Announcement.objects.filter(users=user)
        announcement_count = Announcement.objects.filter(users=user, is_active=True).count()
        return render(request, "mainpage/announcement_page.html",
                      {'customer': customer, 'announcement': announcement, 'announcement_count': announcement_count})


def read_announcement_page(request, username, id):
    user = get_object_or_404(User, username=username)
    if user.is_customer:
        customer = Customer.objects.get(user=user)
        announcement = Announcement.objects.get(users=user, id=id)
        announcement.is_read = True
        announcement.save()
        announcement_count = Announcement.objects.filter(users=user, is_active=True).count()
        return render(request, "mainpage/read_announcement.html",
                      {'customer': customer, 'announcement': announcement, 'announcement_count': announcement_count})


def delete_announcement_page(request, username, id):
    user = get_object_or_404(User, username=username)
    if user.is_customer:
        customer = Customer.objects.get(user=user)
        announcement = Announcement.objects.get(users=user, id=id)
        announcement.is_active = False
        announcement.save()
        return redirect('customer_announcement', user)


def support_page(request, username):
    user = get_object_or_404(User, username=username)
    if user.is_customer:
        customer = Customer.objects.get(user=user)
        room = SupportRoom.objects.filter(user=user)
        announcement_count = Announcement.objects.filter(users=user, is_active=True).count()
        if 'create_support' in request.POST:
            postData = request.POST
            body = postData.get('body')
            new_room = SupportRoom.objects.create(user=request.user)
            new_room.save()

            new_support = Support.objects.create(room_id=new_room.room_id, sender=user, body=body)
            new_support.save()
            return render(request, "mainpage/partials/create_support.html",
                          {'customer': customer, 'room': room, 'announcement_count': announcement_count})
        return render(request, "mainpage/partials/create_support.html",
                      {'customer': customer, 'room': room, 'announcement_count': announcement_count})


def support_page_message(request, username, room_id):
    user = get_object_or_404(User, username=username)
    other_user = get_object_or_404(User, username=username)
    if user.is_customer:
        customer = Customer.objects.get(user=user)
        room = SupportRoom.objects.filter(user=user)
        select_room = SupportRoom.objects.get(user=user, room_id=room_id)
        supports = Support.objects.filter(room_id=room_id)
        answer = AnswerSupport.objects.filter(room_id=room_id)
        announcement_count = Announcement.objects.filter(users=user, is_active=True).count()
        if request.method == 'POST':
            postData = request.POST
            body = postData.get('body')
            msg = Support.objects.create(room_id=room_id, sender=user, body=body)
            msg.save()
            return render(request, "mainpage/partials/support.html",
                          {'customer': customer, 'room': room, 'supports': supports, 'answer': answer,
                           'select_room': select_room, 'announcement_count': announcement_count})
        return render(request, "mainpage/partials/support.html",
                      {'customer': customer, 'room': room, 'supports': supports, 'answer': answer,
                       'select_room': select_room, 'announcement_count': announcement_count})
