from django import forms
from registration.models import UserTypes

CHOICES = (
    (UserTypes.PERSON, 'Quero Doar'),
    (UserTypes.SCHOOL, 'Quero Receber'),
)

class SocialLoginForm(forms.Form):
    email = forms.EmailField(label='E-mail', max_length=255, required=False)
    name = forms.CharField(max_length=255, required=False)
    social_id = forms.CharField(max_length=255)

class UserForm(forms.Form):
    email = forms.EmailField(label='E-mail', max_length=255, required=True)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput, required=True)
    type = forms.CharField(
        max_length=20,
        label='O que deseja realizar?',
        widget=forms.Select(
            choices=CHOICES,
            attrs={
                'required' : True,
            }))

class UserDataForm(forms.Form):
    is_company = forms.BooleanField(widget=forms.HiddenInput, required=False)
    company_name = forms.CharField(label='Razão Social', max_length=20, required=False)
    name = forms.CharField(label='Nome Fantasia', max_length=255)
    registration_number = forms.CharField(label='CNPJ', max_length=18)
    state_registration = forms.CharField(label='Inscrição Estadual', max_length=20, required=False)
    phone_number = forms.CharField(label='Telefone Fixo', max_length=14)
    cell_phone_number = forms.CharField(label='Telefone Celular', max_length=15)

    def _post_clean(self):
        if not self.cleaned_data['is_company']:
            return

        if not self.cleaned_data['company_name']:
            self.add_error('company_name', 'Campo obrigatório')

        if not self.cleaned_data['state_registration']:
            self.add_error('state_registration', 'Campo obrigatório')

class AddressForm(forms.Form):
    zip_code = forms.CharField(label='CEP', max_length=9)
    street = forms.CharField(label='Endereço', max_length=255)
    number = forms.CharField(label='Número', max_length=10)
    complement = forms.CharField(label='Complemento', max_length=255, required=False)
    district = forms.CharField(label='Bairro', max_length=255)
    city = forms.CharField(label='Cidade', max_length=255)
    state = forms.CharField(label='UF', max_length=2)
