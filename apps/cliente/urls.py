from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.principal, name = 'cliente'),
    path('crear_cliente/', views.crear),
    path('modificar_cliente/',views.modificar),
    path('eliminar_cliente/',views.eliminar),
    path('ver_cuenta/',views.ver_cuenta),
    path('clientes', views.ver_cliente),
    path(r'deposito/(?P<numero>d+)/$', views.depositar, name = 'deposito'),
    path(r'retirar/(?P<numero>d+)/$', views.retirar, name = 'retirar'),
    path(r'agregar_cuenta/(?P<numero>d+)/$', views.agregar_cuenta, name = 'agregar_cuenta'),

]