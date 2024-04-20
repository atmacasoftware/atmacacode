from import_export import resources
from supports.models import *

class SupportResourse(resources.ModelResource):
    class Meta:
        model = Support
        fields = (
            'support_id',
            'sender',
            'date',
            'is_read',
        )

class AnswerResourse(resources.ModelResource):
    class Meta:
        model = AnswerSupport
        fields = (
            'answer_id',
            'recipient',
            'date',
        )

