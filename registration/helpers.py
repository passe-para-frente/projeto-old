from django.conf import settings
import requests
import urllib

def get_coordinates(address):
    key = settings.GMAPS_KEY
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'

    params = {
        'address': address,
        'key': key
    }

    encoded_params = urllib.parse.urlencode(params)
    url = f'{base_url}?{encoded_params}'
    
    response = requests.get(url)
    data = response.json()
    
    if len(data['results']) == 0:
        return {'lat': None, 'lng': None}

    return data['results'][0]['geometry']['location']


class UserValidator:
    required_fields = {
        'default': ['name', 'email', 'type', 'registration_number', 'phone_number', 'cell_phone_number', 'address'],
        'company': ['company_name', 'state_registration']
    }

    @classmethod
    def validate(cls, user, validate_company=False):
        errors = []

        for field in cls.required_fields['default']:
            if not cls._validate_field(user, field):
                errors.append(field)

        if not validate_company:
            return errors

        for field in cls.required_fields['company']:
            if not cls._validate_field(user, field):
                errors.append(field)

        return errors

    def _validate_field(user, field):
        value = getattr(user, field)
        return value is not None and value != ''
