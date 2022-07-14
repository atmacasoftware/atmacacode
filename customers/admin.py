from django.contrib import admin

# Register your models here.
from customers.models import Customer,WhyDelete

admin.site.register(Customer)
admin.site.register(WhyDelete)
