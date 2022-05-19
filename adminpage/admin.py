from django.contrib import admin

# Register your models here.
from adminpage.models import AdminUser,Task,Note

admin.site.register(AdminUser)
admin.site.register(Task)
admin.site.register(Note)
