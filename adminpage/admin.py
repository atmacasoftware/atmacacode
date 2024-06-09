from django.contrib import admin

# Register your models here.
from adminpage.models import *

admin.site.register(Task)
admin.site.register(Note)
admin.site.register(Blog)
