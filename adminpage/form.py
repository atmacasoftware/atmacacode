from django import forms
from django.forms import widgets

from adminpage.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task

        fields = ('customer_name','customer_email','customer_phone','task_name','task_price','task_start_date','estimated_deliver_date')
        labels = {
            'customer_name': 'Müşteri İsmi',
            'customer_email': 'Müşteri Email',
            'customer_phone': 'Müşteri Telefonu',
            'task_name': 'Görev İsmi',
            'task_price':'Görev Ücreti',
            'task_start_date':'Görev Başlama Tarihi',
            'estimated_deliver_date':'Tahmini Teslim Tarihi',
        }

        def __init__(self, *args, **kwargs):
            super(TaskForm, self).__init__(*args, **kwargs)
            self.fields['task_start_date'].widget = widgets.EmailInput()