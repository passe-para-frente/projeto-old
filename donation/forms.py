from django import forms
from .models import Sport, Category, MaterialCondition, Donation, Delivery

class DonationItemForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Digite o material para doar', 'autocomplete': 'off'}
        ),
        required=False
    )
    sport_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Digite o esporte', 'autocomplete': 'off'}
        ),
        required=False
    )
    sport = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False
    )
    category = forms.CharField(
        widget=forms.Select(choices=Category.CHOICES),
    )
    condition = forms.CharField(
        widget=forms.Select(choices=MaterialCondition.CHOICES),
    )
    quantity = forms.IntegerField(
        widget=forms.NumberInput(),
        min_value=0
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Observações sobre o material (opcional)'}
        ),
        required=False
    )
    material = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False
    )
    add_another_item = forms.BooleanField(
        initial=False,
        required=False
    )

class SelectSchoolForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Selecione a escola', 'autocomplete': 'off'}
        )
    )
    delivery = forms.CharField(
        widget=forms.Select(choices=Delivery.CHOICES),
        )
    school = forms.IntegerField(
        widget=forms.HiddenInput()
    )
