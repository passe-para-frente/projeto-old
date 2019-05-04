import csv
from django.http import HttpResponse
from django.forms.models import model_to_dict

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_verbose_name = [field.verbose_name for field in meta.fields]
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta.verbose_name_plural)
        writer = csv.writer(response)

        writer.writerow(field_verbose_name)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response

    export_as_csv.short_description = "Exportar Selecionados"
