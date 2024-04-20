from django import forms
from mainpage.models import Contact,Subscribe

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name','email','phone','content']

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ['email']