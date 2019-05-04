from geopy import distance
from .models import Material, Donation, Sport

def get_materials():
    materials = Material.objects.all().order_by('name')
    dictionary = {}

    for material in materials:
        if material.category not in dictionary.keys():
            dictionary[material.category] = []

        dictionary[material.category].append(
            {'name': material.name, 'id': material.id}
        )

    return dictionary

def get_sports():
    sports = Sport.objects.all().order_by('name')
    list = []

    for sport in sports:
        list.append({'id': sport.id, 'name': sport.name})

    return list

def get_donation(id, user):
    donation = Donation.objects.filter(pk=id).filter(donor=user).first()

    if not donation:
        donation = Donation()
        donation.donor = user
        donation.clean()
        donation.save()

    return donation

def build_school_list(user, schools):
    list = []

    for school in schools:
        school_dict = {
            'id': school.id,
            'name': school.name,
            'street': school.address.street,
            'number': school.address.number,
            'district': school.address.district,
            'city': school.address.city,
            'state': school.address.state,
            'distance': calculate_distance(user.address, school.address)
        }

        list.append(school_dict)

    return sorted(list, key=lambda school: school['distance'])

def calculate_distance(user_address, school_address):
    if not user_address.latitude or not user_address.longitude\
        or not school_address.latitude or not school_address.longitude:
        return 0

    user_coordinates = (user_address.latitude, user_address.longitude)
    school_coordinates = (school_address.latitude, school_address.longitude)

    result = distance.vincenty(user_coordinates, school_coordinates)

    return result.km
