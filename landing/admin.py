from django.contrib import admin
from passe_pra_frente.admin import admin_site
from .models import *
from landing.export_data import ExportCsvMixin


class ContactAdmin(admin.ModelAdmin,ExportCsvMixin):
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, object=None):
        return False

    list_display = ('name', 'email')
    actions = ['export_as_csv']
    search_fields = ['name', 'email']

admin_site.register(Contact, ContactAdmin)
