from django import forms

class UserEditForm(forms.Form):
    current_password = forms.CharField(label='Senha Atual', widget=forms.PasswordInput, required=False)
    new_password = forms.CharField(label='Nova Senha', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput)

class UserEditPersonDataForm(forms.Form):
    name = forms.CharField(label='Nome Completo', max_length=255)
    registration_number = forms.CharField(label='CPF', max_length=14)
    phone_number = forms.CharField(label='Telefone', max_length=14)
    cell_phone_number = forms.CharField(label='Celular', max_length=15)