from django.urls import path
from .views import register_user_data,register_address, social_networks_login, render_address

urlpatterns = [
    path('redes', social_networks_login),
    path('dados', register_user_data),
    path('endereco', render_address),
    path('endereco/processamento', register_address, name='register_address')
]
