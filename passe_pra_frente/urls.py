"""passe_pra_frente URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from .admin import admin_site

urlpatterns = [
    path('', include('landing.urls')),
    path('cadastro/', include('registration.urls')),
    path('perfil/', include('user_profile.urls')),
    path('doacao/', include('donation.urls')),
    path('admin/', admin_site.urls),
]
