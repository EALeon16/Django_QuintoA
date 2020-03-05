from django.shortcuts import render, redirect

from .forms import FormularioCliente, FormularioModificarCliente, FormularioTransaccion, FormularioAgregar_Cuenta
from .forms import FormularioCuenta
import datetime
from apps.modelo.models import Cliente, Cuenta, Transaccion
from django.contrib.auth.decorators import login_required

def principal(request):
    lista = Cliente.objects.all().order_by('apellidos')
    context = {
        'lista' : lista,
    }
    return render (request, 'cliente/principal_cliente.html', context)

def ver_cliente(request):
    lista = Cliente.objects.all().order_by('apellidos')
    context = {
        'lista' : lista,
    }
    return render (request, 'cliente/clientes.html', context)

@login_required
def crear(request):
    initial_data = {
        'numero':"111696h-0002" + str(Cliente.objects.count()+1)
    }
    formulario = FormularioCliente(request.POST)
    formularioCuenta = FormularioCuenta(request.POST or None, initial = initial_data)
    usuario = request.user#peticion que es procesada x el frmawor agrega el usuario
    if usuario.groups.filter(name = 'administrativo').exists():

        if request.method == 'POST':
            if formulario.is_valid() and formularioCuenta.is_valid():
                datos = formulario.cleaned_data
                cliente = Cliente()
                cliente.cedula = datos.get('cedula')
                cliente.nombres = datos.get('nombres')
                cliente.apellidos = datos.get('apellidos')
                cliente.genero = datos.get('genero')
                cliente.estadoCivil = datos.get('estadoCivil')
                cliente.fechaNacimiento = datos.get('fechaNacimiento')
                cliente.correo = datos.get('correo')
                cliente.telefono = datos.get('telefono')
                cliente.celular = datos.get('celular')
                cliente.direccion = datos.get('direccion')
                cliente.save()
                datosCuenta = formularioCuenta.cleaned_data #obtiene todos los datos del formulario cuenta
                cuenta = Cuenta()
                cuenta.numero = datosCuenta.get('numero')
                cuenta.estado = True
                cuenta.fechaApertura = datosCuenta.get('fechaApertura')
                cuenta.tipoCuenta = datosCuenta.get('tipoCuenta')
                cuenta.saldo = datosCuenta.get('saldo')
                cuenta.cliente = cliente
                cuenta.save()
                return redirect(principal)

    else:
        return render(request,'cliente/acceso_prohibido.html')
    context = {
        'f': formulario, 
        'fc': formularioCuenta, 
    }
    return render (request, 'cliente/crear_cliente.html', context)



def modificar(request):
    dni = request.GET['cedula']
    cliente = Cliente.objects.get(cedula = dni)
    if request.method == 'POST':
        formulario = FormularioModificarCliente(request.POST)
        if formulario.is_valid():
            datos = formulario.cleaned_data
            cliente.nombres = datos.get('nombres')
            cliente.apellidos = datos.get('apellidos')
            cliente.genero = datos.get('genero')
            cliente.estadoCivil = datos.get('estadoCivil')
            cliente.fechaNacimiento = datos.get('fechaNacimiento')
            cliente.correo = datos.get('correo')
            cliente.telefono = datos.get('telefono')
            cliente.celular = datos.get('celular')
            cliente.direccion = datos.get('direccion')
            cliente.save()
            return redirect(principal)
    else:
        formulario = FormularioModificarCliente(instance = cliente)
    context = {
        'dni': dni,
        'cliente': cliente,
        'formulario': formulario
            }
    
    return render (request, 'cliente/modificar_cliente.html', context)

def eliminar(request):
    dni = request.GET['cedula']
    cliente = Cliente.objects.get(cedula = dni)
    if request.method == 'POST':
        cliente.delete()
        return redirect(ver_cliente)
    else:
        formulario = FormularioModificarCliente(instance = cliente)
    
    context = {
        'dni': dni,
        'cliente': cliente,
        'formulario': formulario
            }
    
    return render (request, 'cliente/eliminar_cliente.html', context)


def ver_cuenta(request):
    dni = request.GET['cedula']
    cliente = Cliente.objects.get(cedula = dni)
    cuenta = Cuenta.objects.filter(cliente_id = cliente.cliente_id)
    
    context = {
        'cuenta' : cuenta,
        'cliente': cliente.nombres + " " + cliente.apellidos
        
    }
    return render (request, 'cuenta/ver_cuenta.html', context)

@login_required
def depositar(request, numero):
    cuenta = Cuenta.objects.get(numero=numero)
    cliente = Cliente.objects.get(cliente_id = cuenta.cliente_id)
    formulario = FormularioTransaccion(request.POST)
    usuario = request.user#peticion que es procesada x el frmawor agrega el usuario
    if usuario.groups.filter(name = 'cajeros').exists():
        if request.method == 'POST':
            if formulario.is_valid():
                datos = formulario.cleaned_data
                cuenta.saldo = cuenta.saldo + datos.get('valor')
                cuenta.save()
                transaccion = Transaccion()
                transaccion.tipo = 'deposito'
                transaccion.valor = datos.get('valor')
                transaccion.descripcion = datos.get('descripcion')
                transaccion.responsable = 'xxxxxxxxx'
                transaccion.cuenta = cuenta
                transaccion.save()
                deposito = float(datos.get('valor'))
                mensaje = 'Transaccion exitosa'
                return render(request, 'transaccion/status.html', locals())
    else:
        return render(request,'cliente/acceso_prohibido.html')
            
    
    context = {
        'cuenta': cuenta,
        'formulario': formulario,
        'cliente': cliente
        
    }
    return render (request, 'transaccion/depositar.html', context)

def retirar(request, numero):
    cuenta = Cuenta.objects.get(numero=numero)
    cliente = Cliente.objects.get(cliente_id = cuenta.cliente_id)
    formulario = FormularioTransaccion(request.POST)
    usuario = request.user#peticion que es procesada x el frmawor agrega el usuario
    if usuario.groups.filter(name = 'cajeros').exists():
        if request.method == 'POST':
            if formulario.is_valid():
                datos = formulario.cleaned_data
                cuenta.saldo = cuenta.saldo - datos.get('valor')
                cuenta.save()
                transaccion = Transaccion()
                transaccion.tipo = 'deposito'
                transaccion.valor = datos.get('valor')
                transaccion.descripcion = datos.get('descripcion')
                transaccion.responsable = 'xxxxxxxxx'
                transaccion.cuenta = cuenta
                transaccion.save()
                deposito = float(datos.get('valor'))
                mensaje = 'Transaccion exitosa'
                return render(request, 'transaccion/status.html', locals())
    else:
        return render(request,'cliente/acceso_prohibido.html')
            
    context = {
            'cuenta': cuenta,
            'formulario': formulario,
            'cliente': cliente
        
    }
    return render (request, 'transaccion/retirar.html', context)

    

def agregar_cuenta(request):

    f = datetime.date.today()
    formato = f.strftime("%Y-%m-%d")
    personas = request.GET['id']
    initial_data = {
        'numero':"111696h-0002" + str(Cliente.objects.count()+1),
    }
    persona = Cliente.objects.get(cliente_id = personas)
    listaC = Cuenta.objects.get(cliente_id = personas)
    formularioCuenta = FormularioCuenta(request.POST or None, initial = initial_data)
    if request.method == 'POST':
        if formularioCuenta.is_valid():
            datosCuenta = formularioCuenta.cleaned_data #obtiene todos los datos del formulario cuenta
            cuenta = Cuenta()
            cuenta.numero = datosCuenta.get('numero')
            cuenta.estado = True
            cuenta.fechaApertura = datosCuenta.get('fechaApertura')
            cuenta.tipoCuenta = datosCuenta.get('tipoCuenta')
            cuenta.saldo = datosCuenta.get('saldo')
            cuenta.cliente = persona
            cuenta.save()
            return redirect('/cliente')
        else:
            print("Error")    
    context = {
        'listaC': listaC,
        'formato': formato,
        'persona': persona,
        'numeroC':"111696h-0001" + str(Cliente.objects.count()+1),
        'fc': formularioCuenta,
    }


    
    return render (request, 'cuenta/agregar_cuenta.html', context)
    
    