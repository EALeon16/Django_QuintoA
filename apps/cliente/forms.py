from django import forms 
from apps.modelo.models import Cliente, Cuenta, Transaccion

class FormularioCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["cedula", "nombres", "apellidos",  "genero", "fechaNacimiento","estadoCivil","correo","telefono", "celular", "direccion"]


class FormularioModificarCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombres", "apellidos",  "genero", "fechaNacimiento","estadoCivil","correo","telefono", "celular", "direccion"]

class FormularioCuenta(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ["numero", "tipoCuenta", "saldo"]
        readonly_fields = ['numero']
        
       
        
class FormularioTransaccion(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = [ "valor","descripcion"]

class FormularioAgregar_Cuenta(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ["numero", "tipoCuenta", "saldo"]
        readonly_fields = ['numero']