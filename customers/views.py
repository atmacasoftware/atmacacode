from random import randint

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from unidecode import unidecode

from customers.decorators import custom_login_required
from customers.models import Customer
from user_accounts.models import Account


def customer_login(request):
    return render(request,'mainpage/login.html')

def customer_register(request):
    return render(request,'mainpage/register.html')

class Signup(View):
    def get(self, request):
        return render(request, 'customer/register.html')

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
            return redirect('index')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'customer/register.html', data)

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
        return render(request, 'customer/login.html')

    def post(self, request):
        email = request.POST.get('email-signin')
        password = request.POST.get('password-signin')

        try:
            customer = Customer.get_customer_by_email(email)
            print(customer.user)
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
                        return redirect('index')
                else:
                    error_message = 'Email or Password invalid !!'

            else:
                error_message = 'Email or Password invalid !!'
                return JsonResponse({'data': 'Kullanıcı adı veya şifre yanlış!'})
            return redirect('index')
        except:
            return JsonResponse({'data': 'Email ve şifre alanlarının doldurulması gerekmektedir.'})


@custom_login_required
def logout(request):
    request.session.clear()
    return redirect('index')