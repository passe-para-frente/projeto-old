from django.contrib import admin
from passe_pra_frente.admin import admin_site
from .models import User, Address
from landing.export_data import ExportCsvMixin

class UserAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ("name" ,"email", "type")
    search_fields = ['name', 'email']
    actions = ['export_as_csv']
    list_filter = ['type']

    class Meta:
        model = User

    exclude = ('last_login', 'groups', 'first_name', 'last_name',
    'is_superuser', 'date_joined')

admin_site.register(User, UserAdmin)

class AddressAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('user', 'street', 'city', 'zip_code', 'district')
    search_fields = ['user__name', 'user__email']
    actions = ['export_as_csv']
    list_filter = ['user__type', 'city', 'district', ]

    class Meta:
        model = Address

admin_site.register(Address, AddressAdmin)
