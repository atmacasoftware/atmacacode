from django.contrib import admin

# Register your models here.
from adminpage.models import AdminUser

admin.site.register(AdminUser)
