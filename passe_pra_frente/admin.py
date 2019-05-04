from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    site_header = 'Passe pra Frente'

admin_site = MyAdminSite(name='myadmin')