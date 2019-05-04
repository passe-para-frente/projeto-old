from django.urls import path
from .views import add_item, select_school, confirm_donation, user_donations, get_schools, delete_item, school_donations, success_page

app_name = 'donation'

urlpatterns = [
    path('', add_item),
    path('<int:id>', add_item, name='add_item'),
    path('escolas', get_schools),
    path('selecionar-escola/<int:id>', select_school, name='select_school'),
    path('confirmar/<int:id>', confirm_donation, name='confirm_donation'),
    path('deletear-item/<int:id>/<int:item_id>', delete_item, name='delete_item'),
    path('sucesso', success_page, name='success_page'),
    path('minhas-doacoes', user_donations, name='user_donations'),
    path('escola-doacoes', school_donations, name='school_donations'),
]