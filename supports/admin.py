from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from supports.resources import *
# Register your models here.
from supports.models import Support,AnswerSupport,SupportRoom

class SupportAdmin(ImportExportModelAdmin):
    list_display = ('support_id','sender','date','is_read')
    resource_class = SupportResourse

class AnswerAdmin(ImportExportModelAdmin):
    list_display = ('answer_id','recipient','date')
    resource_class = SupportResourse

admin.site.register(SupportRoom)
admin.site.register(Support,SupportAdmin)
admin.site.register(AnswerSupport,AnswerAdmin)
