from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from passe_pra_frente.admin import admin_site
from .models import Sport, Donation, Material, DonationItem
from landing.export_data import ExportCsvMixin

class DonationAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('donor', 'school', 'created_at')
    fields = ('created_at', 'donor', 'school', 'delivery', 'confirmed', 'donation_items')
    readonly_fields = ('created_at', 'donation_items')
    actions = ['export_as_csv']
    list_filter = ['created_at', 'donor', 'school']
    search_fields = ['donor__registration_number', 'donor__name', 'donor__email']

    class Meta:
        model = Donation

    def donation_items(self, instance):
        return format_html_join(
            mark_safe('<br>'),
            '{}',
            ((item,) for item in instance.donationitem_set.all()),
        ) or mark_safe("<span class='errors'> -- </span>")

    donation_items.short_description = "Materiais"

admin_site.register(Donation, DonationAdmin)

class SportAdmin(admin.ModelAdmin, ExportCsvMixin):
    ordering = ('name',)
    actions = ['export_as_csv']
    search_fields = ['name']
    list_display = ['name']
    list_filter = ['name']

admin_site.register(Sport, SportAdmin)

class MaterialAdmin(admin.ModelAdmin, ExportCsvMixin):
    ordering = ('name',)
    actions = ['export_as_csv']
    search_fields = ['name', 'category', 'sport']
    list_filter = ['name', 'category', 'sport']
    list_display = ['name', 'category', 'sport']


admin_site.register(Material, MaterialAdmin)

class DonationItemAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['donation', 'category', 'material', 'sport', 'condition', 'quantity']
    actions = ['export_as_csv']
    search_fields = ['donation__donor__name',
                     'category',
                     'material__name',
                     'sport__name',
                     'condition',
                     'quantity',
                     'description']
    list_filter = ['donation__created_at',
                   'category',
                   'material',
                   'sport',
                   'condition',
                   'quantity',
                   'donation']

admin_site.register(DonationItem, DonationItemAdmin)
