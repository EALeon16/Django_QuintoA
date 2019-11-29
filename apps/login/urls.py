
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.ingresar, name = 'autenticar'),
    path('logout', views.cerrar, name = 'cerrar_sesion'),
    
]