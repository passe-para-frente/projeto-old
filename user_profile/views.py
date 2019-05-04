from django.shortcuts import render
from registration.forms import UserDataForm, AddressForm
from .forms import UserEditForm, UserEditPersonDataForm
from registration.models import Address, User
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def user_profile(request):
    page_name = 'perfil'
    return render(request, 'user-profile.html', {'page_name': page_name, 'footer_menu': True})


def edit_user(request):
    page_name = 'editar perfil'
    form = UserEditForm(request.POST or None)
    user = request.user
    success_message = False

    if request.method == 'POST':
        if form.data['new_password'] != form.data['confirm_password']:
            form.add_error('confirm_password', 'As senhas não conferem')

        if not user.check_password(form.data['current_password']):
            form.add_error('current_password', 'Senha inválida')

    if form.is_valid():
        user.set_password(form.data['new_password'])
        user.save()

        success_message = True


    return render(request, 'edit-user.html', {'form': form, 'page_name': page_name, 'success_message':success_message})


def edit_data(request):
    user = request.user
    page_name = 'editar perfil'
    success_message = False

    if user.type == 'PERSON':
        form = UserEditPersonDataForm(request.POST or None)
        form.fields['name'].initial = request.user.name
        form.fields['registration_number'].initial = user.registration_number
        form.fields['phone_number'].initial = user.phone_number
        form.fields['cell_phone_number'].initial = user.cell_phone_number

        if form.is_valid():
            user.name = form.cleaned_data['name']
            user.registration_number = form.cleaned_data['registration_number']
            user.phone_number =form.cleaned_data['phone_number']
            user.cell_phone_number = form.cleaned_data['cell_phone_number']

            user.save()

            success_message = True
    else:
        form = UserDataForm(request.POST or None)
        form.fields['company_name'].initial = user.company_name
        form.fields['name'].initial = request.user.name
        form.fields['registration_number'].initial = user.registration_number
        form.fields['state_registration'].initial = user.state_registration
        form.fields['phone_number'].initial = user.phone_number
        form.fields['cell_phone_number'].initial = user.cell_phone_number

        if form.is_valid():
            user.company_name = form.cleaned_data['company_name']
            user.name = form.cleaned_data['name']
            user.registration_number = form.cleaned_data['registration_number']
            user.state_registration = form.cleaned_data['state_registration']
            user.phone_number = form.cleaned_data['phone_number']
            user.cell_phone_number = form.cleaned_data['cell_phone_number']

            user.save()

            success_message = True

    return render(request, 'edit-data.html', {'form': form, 'page_name': page_name, 'success_message':success_message})


def edit_address(request):
    page_name = 'editar perfil'
    form = AddressForm(request.POST or None)
    success_message = False
    user = request.user
    address = Address.objects.filter(user=user).first()

    if address != None:
        form.fields['zip_code'].initial = address.zip_code
        form.fields['street'].initial = address.street
        form.fields['number'].initial = address.number
        form.fields['complement'].initial = address.complement
        form.fields['district'].initial = address.district
        form.fields['city'].initial = address.city
        form.fields['state'].initial = address.state

    if request.method == 'POST' and form.is_valid():

        if address is None:
            address = Address()

        address.zip_code = form.cleaned_data['zip_code']
        address.street = form.cleaned_data['street']
        address.number = form.cleaned_data['number']
        address.complement = form.cleaned_data['complement']
        address.district = form.cleaned_data['district']
        address.city = form.cleaned_data['city']
        address.state = form.cleaned_data['state']
        address.user = user

        address.save()

        success_message = True

    return render(request, 'edit-address.html', {'form': form, 'page_name': page_name, 'success_message':success_message})
