from random import randint

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views import View
from unidecode import unidecode

from announcement.models import Announcement
from customers.decorators import custom_login_required
from customers.forms import CustomerProfileUpdateForm
from customers.models import Customer, WhyDelete
from order.models import Order
from user_accounts.models import Account


def customer_login(request):
    return render(request, 'mainpage/login.html')


def customer_register(request):
    return render(request, 'mainpage/register.html')


class Signup(View):
    def get(self, request):
        return render(request, 'mainpage/register.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password1')
        extra = str(randint(1, 10000000))
        username = unidecode(first_name) + unidecode(last_name) + "-" + extra
        haspass = make_password(password)
        user = Account(username=username, password=haspass, email=email, first_name=first_name, last_name=last_name)
        user.is_customer = True
        user.save()
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password,
                            user=user)
        error_message = self.validateCustomer(customer)

        if not error_message:
            customer.password = make_password(customer.password)
            customer.save()

            current_site = get_current_site(request)
            # mail_subject = "Hesabınız başarıyla oluşturuldu. E-DurmaAl'ın eşsiz fırsat ve kampanyalar dünyasında gezinmek için hemen giriş yapın. Keyifli Alışverişler."
            # message = render_to_string('customer/sendMessage/register_message.html', {
            #    'customer': customer,
            #    'domain': current_site,
            #    'uid': urlsafe_base64_encode(force_bytes(customer.pk)),
            # })
            # to_email = email
            # send_mail = EmailMessage(mail_subject, message, to=[to_email])
            # send_mail.send()
            return redirect('mainpage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'mainpage/register.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "İsim yazmanı gerekmektedir."
        elif len(customer.first_name) < 3:
            error_message = "İsim en az 3 kelime olmalıdır."
        elif not customer.last_name:
            error_message = "Soyisim gereklidir."
        elif len(customer.last_name) < 3:
            error_message = "Soyisim en az 3 kelime olmalıdır."
        elif not customer.phone:
            error_message = "Telefon numarasını gereklidir."
        elif len(customer.phone) < 11:
            error_message = "Telefon numarası en az 11 rakam olmalıdır."
        elif customer.isExists():
            error_message = 'Email adresi sistem mevcut.'

        return error_message


class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'mainpage/login.html')

    def post(self, request):
        email = request.POST.get('customer-email')
        password = request.POST.get('customer-password')

        try:
            customer = Customer.get_customer_by_email(email)
            user = authenticate(username=customer.user, password=password)
            login(request, user)
            error_message = None
            if customer:
                flag = check_password(password, user.password)
                if flag:
                    request.session['customer'] = customer.id
                    request.session['email'] = email
                    request.session['first_name'] = customer.first_name
                    request.session['last_name'] = customer.last_name

                    if Login.return_url:
                        return HttpResponseRedirect(Login.return_url)
                    else:
                        Login.return_url = None
                        return redirect('mainpage')
                else:
                    error_message = 'Email or Password invalid !!'
            else:
                return render(request, "mainpage/login.html", {'error': 'Kullanıcı Adı veya Şifre Hatalı!'})
            return redirect('mainpage')
        except:
            return render(request, "mainpage/login.html", {'error': 'Kullanıcı Adı veya Şifre Hatalı!'})


@login_required
def logout(request):
    request.session.clear()
    return redirect('mainpage')


@login_required
def profile_page(request, username):
    user = get_object_or_404(Account, username=username)
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
                                  {'customer': customer, 'update_form': update_form,'announcement_count':announcement_count})

                else:
                    return render(request, "mainpage/customer_edit.html",
                                  {'customer': customer, 'update_form': update_form,'announcement_count':announcement_count})
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
                                           'delete_error': delete_error,'announcement_count':announcement_count})
                else:
                    delete_error = "Mevcut şifre boş bırakılamaz!"
                    return render(request, "mainpage/customer_edit.html",
                                  {'customer': customer, 'update_form': update_form, 'delete_error': delete_error,'announcement_count':announcement_count})
            else:
                return render(request, "mainpage/customer_edit.html",
                              {'customer': customer, 'update_form': update_form,'announcement_count':announcement_count})
        except:
            pass
        return render(request, "mainpage/customer_edit.html", {'customer': customer, 'update_form': update_form,'announcement_count':announcement_count})
    else:
        redirect("mainpage")


def order_page(request, username):
    user = get_object_or_404(Account, username=username)
    if user.is_customer:
        customer = Customer.objects.get(user=user)
        orders = Order.objects.filter(customer=customer)
        announcement_count = Announcement.objects.filter(users=user, is_active=True).count()
        return render(request, "mainpage/order_page.html", {'customer': customer, 'orders': orders,'announcement_count':announcement_count})

def announcement_page(request, username):
    user = get_object_or_404(Account, username=username)
    if user.is_customer:
        customer = Customer.objects.get(user=user)
        announcement = Announcement.objects.filter(users=user)
        announcement_count = Announcement.objects.filter(users=user, is_active=True).count()
        return render(request, "mainpage/announcement_page.html", {'customer': customer, 'announcement': announcement,'announcement_count':announcement_count})

def read_announcement_page(request, username,id):
    user = get_object_or_404(Account, username=username)
    if user.is_customer:
        customer = Customer.objects.get(user=user)
        announcement = Announcement.objects.get(users=user, id=id)
        announcement.is_read = True
        announcement.save()
        announcement_count = Announcement.objects.filter(users=user, is_active=True).count()
        return render(request, "mainpage/read_announcement.html", {'customer': customer, 'announcement': announcement,'announcement_count':announcement_count})

def delete_announcement_page(request, username, id):
    user = get_object_or_404(Account, username=username)
    if user.is_customer:
        customer = Customer.objects.get(user=user)
        announcement = Announcement.objects.get(users=user, id=id)
        announcement.is_active = False
        announcement.save()
        return redirect('customer_announcement',user)
