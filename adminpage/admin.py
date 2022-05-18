from django.contrib import admin

# Register your models here.
from adminpage.models import AdminUser,Task

admin.site.register(AdminUser)
admin.site.register(Task)
