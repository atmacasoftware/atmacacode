from django.shortcuts import redirect
from customers.models import Customer


def custom_login_required(function):
    def wrap(request, *args, **kwargs):
        session = request.session # this is a dictionary with session keys
        customer = Customer.objects.all()
        user = request.user
        try:
            customer = request.session['customer']
            if customer:
                # the decorator is passed and you can handle the request from the view
                return function(request, *args, **kwargs)
        except:
            return redirect('login')


    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap