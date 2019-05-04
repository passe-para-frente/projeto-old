from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from registration.models import User, UserTypes, Address, User
from registration.helpers import UserValidator
from .models import Donation, DonationItem, Material, Category, Sport
from .forms import DonationItemForm, SelectSchoolForm
from .helpers import get_donation, get_materials, get_sports, build_school_list
import json

def _render_add_item_page(request, form):
    page_name = 'doação'
    materials = get_materials()
    sports = get_sports()

    return render(request, 'add-item.html', {
        'form': form,
        'materials': materials,
        'sports': sports,
        'page_name': page_name,
        'footer_menu': True
    })

@login_required
def add_item(request, id=None):
    form = DonationItemForm(request.POST or None)

    errors = UserValidator.validate(request.user)

    if len(errors) > 0:
        return redirect(f'/cadastro/dados')

    if form.is_valid():
        material_id = form.cleaned_data['material']
        category = form.cleaned_data['category']
        donation = get_donation(id, request.user)
        sport = Sport.objects.filter(name=form.cleaned_data['sport']).first()
        material = Material.objects.filter(pk=material_id).first()

        if not Category.is_empty(category) and not material:
            form.add_error(None, 'Material não encontrado')
            return _render_add_item_page(request, form)

        item = DonationItem()
        item.category = category
        item.condition = form.cleaned_data['condition']
        item.quantity = form.cleaned_data['quantity']
        item.description = form.cleaned_data['description']
        item.donation = donation
        item.sport = sport
        item.material = material

        item.save()

        if form.cleaned_data['add_another_item']:
            return redirect(f'/doacao/{donation.id}')

        return redirect(f'/doacao/selecionar-escola/{donation.id}')

    return _render_add_item_page(request, form)

@login_required
def select_school(request, id):
    page_name = 'doação'
    schools = get_schools(request)
    form = SelectSchoolForm(request.POST or None)
    donation = get_donation(id, request.user)
    if not donation:
        return redirect('/doacao')

    if form.is_valid():
        school_id = form.cleaned_data['school']
        school = User.objects.filter(
            pk=school_id,
            type=UserTypes.SCHOOL
        ).first()

        if not school:
            form.add_error(None, 'Escola não encontrada')
            return render(request, 'select-school.html', {'form': form})

        donation.delivery = form.cleaned_data['delivery']
        donation.school = school
        donation.save()

        return redirect(f'/doacao/confirmar/{donation.id}')

    content={
        'form': form,
        'page_name': page_name,
        'donation':donation,
        'schools': schools,
        'footer_menu': True
    }

    return render(request, 'select-school.html', content)

@login_required
def confirm_donation(request, id):
    page_name = 'doação'
    donation = get_donation(id, request.user)

    if not donation:
        return redirect('/doacao')

    if request.method == 'POST':
        donation.confirmed = True
        donation.save()

        return redirect('donation:success_page')

    items = donation.donationitem_set.all()

    count_items = items.count()

    content={
        'donation': donation,
        'items': items,
        'count_items': count_items,
        'page_name': page_name,
        'footer_menu': True
    }

    return render(request, 'confirm-data.html', content)

@login_required
def delete_item(request, id, item_id):
    donation = get_donation(id, request.user)

    donation_item = donation.donationitem_set.filter(id=item_id).first()

    if donation_item:
        donation_item.delete()

    content={
        'donation': donation,
    }

    return redirect('donation:confirm_donation', id=donation.id)

def get_schools(request):
    query = User.objects.filter(type='SCHOOL').all()

    if 'name' in request.GET:
        query = query.filter(name__icontains=request.GET['name'])

    schools = query.all()

    list = build_school_list(request.user, schools)

    return JsonResponse(list, safe=False)

def user_donations(request):
    page_name = 'minhas doações'
    donations = Donation.objects\
        .filter(donor_id=request.user.id)\
        .filter(confirmed=True)\
        .all()

    donations_count = donations.count()
    content = {'donations': donations, 'donations_count': donations_count, 'page_name': page_name, 'footer_menu': True}

    return render(request, 'user-donations.html', content)

def school_donations(request):
    donations = Donation.objects\
        .filter(school_id=request.user.id)\
        .filter(confirmed=True)\
        .all()

    donations_count = donations.count()
    user_type = request.user.type

    content = {'user_type':user_type, 'donations':donations, 'donations_count':donations_count, 'footer_menu': True}
    return render(request, 'user-donations.html', content)

def success_page(request):
    donation = Donation.objects\
        .filter(donor_id=request.user.id)\
        .last()

    content = {'donation':donation, 'footer_menu': False}

    return render(request, 'success-page.html', content)
