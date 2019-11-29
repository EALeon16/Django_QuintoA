from django.contrib import admin
from .models import Cliente
from .models import Cuenta
from .models import Transaccion

class AdminCliente(admin.ModelAdmin):
	list_display = ["cedula", "apellidos", "nombres","genero","celular"]
	list_editable = ["apellidos", "nombres"]
	list_filter = ["genero","estadoCivil"]
	search_fields = ["cedula","apellidos"]
	class Meta:
		model = Cliente

admin.site.register(Cliente, AdminCliente)

class AdminCuenta(admin.ModelAdmin):
	list_display = ["cliente", "numero", "estado","saldo"]
	list_filter = ["cliente","numero","estado"]
	search_fields = ["numero","cliente"]
	class Meta:
		model = Cuenta

admin.site.register(Cuenta, AdminCuenta)

class AdminTransaccion(admin.ModelAdmin):
	list_display = ["fechaTransaccion", "tipo", "descripcion", "responsable"]
	list_filter = ["fechaTransaccion", "tipo"]
	search_fields = ["fechaTransaccion","tipo"]
	class Meta:
		model = Transaccion

admin.site.register(Transaccion, AdminTransaccion)

