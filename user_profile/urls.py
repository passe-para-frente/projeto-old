from django.urls import path
from .views import user_profile, edit_user, edit_data, edit_address

urlpatterns = [
    path('', user_profile),
    path('senha', edit_user),
    path('dados', edit_data),
    path('endereco', edit_address)
]