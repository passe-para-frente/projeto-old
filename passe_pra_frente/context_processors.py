from django.conf import settings

def environment_variables(request):
    return {
        'GMAPS_KEY': settings.GMAPS_KEY,
        'FACEBOOK_ID': settings.FACEBOOK_ID,
        'GOOGLE_SIGNIN_ID': settings.GOOGLE_SIGNIN_ID
    }