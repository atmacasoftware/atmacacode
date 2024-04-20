from django import forms
from customers.models import *

class CustomerProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput, required=False)
    last_name = forms.CharField(widget=forms.TextInput, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = Customer
        fields = ['first_name','last_name','phone','email',]

    widgets = {
        'phone':forms.NumberInput(attrs={'max': 15, 'min': 15, 'required': True, 'type': 'number',}),
    }