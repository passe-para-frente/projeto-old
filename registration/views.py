from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from .forms import UserForm, UserDataForm, AddressForm, SocialLoginForm
from .models import UserTypes, Address, User
from .helpers import get_coordinates
from django.http import JsonResponse
from django.contrib import messages
import json


def social_networks_login(request):
    data = json.loads(request.body)
    form = SocialLoginForm(data)

    if not form.is_valid():
        return JsonResponse(form.errors, status=400)

    user = User.objects.filter(social_id=data['social_id']).first()

    if not user:
        user = User()
        user.email = form.cleaned_data['email'] or form.cleaned_data['social_id']
        user.type = UserTypes.PERSON
        user.social_id = form.cleaned_data['social_id']
        user.name = form.cleaned_data['name']
        user.save()
    login(request, user)

    return JsonResponse({}, status=200)


def register_user_data(request):
    page_name = 'cadastro'

    if not request.user.is_authenticated:
        return redirect('/')

    form = UserDataForm(request.POST or None)

    if request.user.is_social_account:
        form.initial = {'name':  request.user.name}

    if request.method == 'POST' and form.is_valid():
        user = request.user
        user.company_name = form.cleaned_data['company_name']
        user.name = form.cleaned_data['name']
        user.registration_number = form.cleaned_data['registration_number']
        user.state_registration = form.cleaned_data['state_registration']
        user.phone_number = form.cleaned_data['phone_number']
        user.cell_phone_number = form.cleaned_data['cell_phone_number']

        if user.type != UserTypes.SCHOOL and request.POST['user_type']:
            user.type = request.POST['user_type']
        try:
            user.save()
        except Exception as e:
            messages.info(request, 'Erro ao enviar seus dados, este CPF/CNPJ já existe em nossa base')
            return redirect('/cadastro/dados')

        return redirect('/cadastro/endereco')

    return render(request, 'user-data.html', {'form': form, 'page_name': page_name, 'footer_menu': False})

def render_address(request):
    if not request.user.is_authenticated:
        return redirect('/')
    form = AddressForm()
    return render(request, 'address.html', {'form': form, 'footer_menu': False})

def register_address(request):
    if not request.user.is_authenticated:
        return redirect('/')

    form = AddressForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = request.user
        existent_address = Address.objects.filter(user=user).first()

        if existent_address is None:
            address = Address()
            address.street = form.cleaned_data['street']
            address.number = form.cleaned_data['number']
            address.complement = form.cleaned_data['complement']
            address.district = form.cleaned_data['district']
            address.city = form.cleaned_data['city']
            address.state = form.cleaned_data['state']
            address.zip_code = form.cleaned_data['zip_code']
            address.user = user
            coordinates = get_coordinates(address)
            address.latitude = coordinates['lat']
            address.longitude = coordinates['lng']
            address.save()
        else:
            existent_address.street = form.cleaned_data['street']
            existent_address.number = form.cleaned_data['number']
            existent_address.complement = form.cleaned_data['complement']
            existent_address.district = form.cleaned_data['district']
            existent_address.city = form.cleaned_data['city']
            existent_address.state = form.cleaned_data['state']
            existent_address.zip_code = form.cleaned_data['zip_code']
            coordinates = get_coordinates(existent_address)
            existent_address.latitude = coordinates['lat']
            existent_address.longitude = coordinates['lng']
            existent_address.save()

        if user.type != 'SCHOOL':
            return redirect('/doacao/')

        messages.info(request, 'Obrigado pelo cadastro da escola.')
        return redirect('/')

    messages.info(request, 'Erro ao enviar seus dados, verifique e tente novamente.')
    return redirect(register_address)
