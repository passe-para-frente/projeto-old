from django import forms
from django.forms import ModelForm
from registration.models import UserTypes
from .models import *

class LoginForm(forms.Form):
    email = forms.EmailField(label='E-mail', max_length=255)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'name',
            'email',
            'message'
        ]

    name = forms.CharField(
        label='Nome', widget=forms.TextInput, max_length=50
    )
    email = forms.EmailField(
        label='E-mail', widget=forms.EmailInput, max_length=255
    )
    message = forms.CharField(
        label='Mensagem', widget=forms.Textarea
    )
