from random import randint

from unidecode import unidecode
from django.contrib.auth.hashers import make_password
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
    return render(request, "adminpage/signin.html")


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
    pass