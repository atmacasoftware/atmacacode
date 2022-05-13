from random import randint

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse
from unidecode import unidecode
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.
from django.template.loader import get_template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View

from adminpage.models import AdminUser
from user_accounts.models import Account


def admin_main_page(request):
    return render(request, "adminpage/mainpage.html")

def singin_page(request):
    pass

class SignupAdmin(View):
    def get(self, request):
        if 'username' in request.session:
            return redirect('mainpage')
        return render(request, 'adminpage/signup.html')

    def post(self, request):
        if 'username' in request.session:
            return redirect('mainpage')
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        address = postData.get('address')
        password = postData.get('password')
        haspass = make_password(password)
        extra = str(randint(1, 10000000))
        username = unidecode(first_name) + unidecode(last_name) + "-" + extra
        user = Account(username=username, password=haspass, email=email, first_name=first_name,
                       last_name=last_name)

        user.is_standartshop = True
        user.save()

        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'username': username,
        }
        error_message = None

        admin_user = AdminUser(authorizedperson=user, first_name=first_name, last_name=last_name,
                                                  phone=phone, email=email, password=password,is_exist=True, is_admin=True,address=address)
        error_message = self.validateCustomer(admin_user)

        if not error_message:
            admin_user.password = make_password(admin_user.password)
            admin_user.save()

            return redirect('admin_login')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            user.delete()

            return render(request, 'adminpage/signup.html', data)

    def validateCustomer(self, admin_user):
        error_message = None
        if (not admin_user.first_name):
            error_message = "İsim yazmanı gerekmektedir."
        elif len(admin_user.first_name) < 2:
            error_message = "İsim en az 3 kelime olmalıdır."
        elif not admin_user.last_name:
            error_message = "Soyisim gereklidir."
        elif len(admin_user.last_name) < 2:
            error_message = "Soyisim en az 3 kelime olmalıdır."
        elif not admin_user.phone:
            error_message = "Telefon numarasını gereklidir."
        elif len(admin_user.phone) < 10:
            error_message = "Telefon numarası en az 10 rakam olmalıdır."

        return error_message


class SigninAdmin(View):
    return_url = None

    def get(self, request):
        SigninAdmin.return_url = request.GET.get('return_url')
        return render(request, 'adminpage/mainpage.html')

    def post(self, request):
        email = request.POST.get('email-signin')
        password = request.POST.get('password-signin')

        try:
            admin = AdminUser.get_admin_by_email(email)
            user = authenticate(username=admin.user, password=password)
            login(request, user)
            error_message = None
            if admin:
                flag = check_password(password, user.password)
                if flag:
                    request.session['customer'] = admin.id
                    request.session['email'] = email
                    request.session['first_name'] = admin.first_name
                    request.session['last_name'] = admin.last_name

                    if SigninAdmin.return_url:
                        return HttpResponseRedirect(SigninAdmin.return_url)
                    else:
                        SigninAdmin.return_url = None
                        return redirect('index')
                else:
                    error_message = 'Email or Password invalid !!'

            else:
                error_message = 'Email or Password invalid !!'
                return JsonResponse({'data': 'Kullanıcı adı veya şifre yanlış!'})
            return redirect('index')
        except:
            return JsonResponse({'data': 'Email ve şifre alanlarının doldurulması gerekmektedir.'})
