# -*- encoding: utf-8 -*-
# Autores: Grupo A - Grupo B
#Nombre del Archivo: views.py
#Codificación: UTF-8
#Descripción: Archivo donde se registran las vistas que atenderan la logica del modulo.
#Notas/Pendientes: Validar que las variables que se obtienen de las sesiones no sean nulas antes de usarlas.


from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
import datetime, random, string
from .models import *

from django.contrib.auth.forms import UserCreationForm
from django.core.mail import EmailMessage, EmailMultiAlternatives

"""
Autor: Pedro Iñiguez
Nombre de función:  registro_institucion
Parámetros: request GET o POST
Salida: Pagina para el Ingreso de codigo si es GET, debe devolver perfil de la institucion creada.
Descripción: Corresponde a la creacion de la institucion y el anexo con e usuario por medio de membresia,
			 asi como update a la tabla peticion con valor 1 pues se usa el codigo.
"""


@login_required
def registro_institucion(request):
    if request.method == 'GET':
        session = request.session['id_usuario']  #Error 10, usar sesion o algun otro
        usuario = Perfil.objects.get(id=session)
        args = {}

        if usuario is not None:
            args['usuario'] = usuario

        else:
            args['error'] = "Error al cargar los datos"

        args.update(csrf(request))
        return render_to_response('Institucion_Sign-up.html', args)
    else:
        print "es post"  #No olvidar borrar los codigos referencia luego.
        try:
            peticion = Peticion.objects.all().filter(fk_usuario=request.session['id_usuario']).first()
            if (peticion.usado == 0):

                siglas = request.POST['siglaInstitucion']
                desc = request.POST['descInstitucion']  #Error 10, usar palabras completas no abreviaturas
                mision = request.POST['misionInstitucion']
                recursos = request.POST['recursosInstitucion']
                web = request.POST['webInstitucion']  #Error 10, usar palabras en español
                correo = request.POST['emailInstitucion']  #Error, 10 usar palabras en español
                telefono = request.POST['telefonoInstitucion']
                cargo = request.POST['cargoInstitucion']
                cargo_desc = request.POST['cargoDescInstitucion'] #Error 10, usar palabras completas no abreviaturas
                ciudad = City.objects.get(id=request.POST['ciudadInstitucion'])
                pais = Country.objects.get(id=request.POST['paisInstitucion'])

                try:
                    image = request.FILES['logo']  #Error 10, usar palabras en español
                except:
                    image = "noPicture.png" #Error 10, usar palabras en español

                insti = Institucion();  #Error 10, usar palabras completas no abreviaturas
                #Error 1, punto y coma por que?
                insti.nombre = peticion.nombre_institucion
                insti.siglas = siglas
                insti.descripcion = desc
                insti.mision = mision
                insti.web = web  #Error 10, usar palabras en español
                insti.recursos_ofrecidos = recursos
                insti.correo = correo
                insti.telefono_contacto = telefono
                insti.ciudad = ciudad
                insti.pais = pais
                insti.save()
                insti.logo = image #Error 10, usar palabras en español
                insti.save()

                peticion.usado = 1
                peticion.save()

                membresia = Membresia()
                membresia.es_administrator = 1  #Error 10, usar palabras en español
                membresia.cargo = cargo
                membresia.descripcion_cargo = cargo_desc  #Error 10, usar palabras completas no abreviaturas
                membresia.fecha_peticion = datetime.datetime.now()
                membresia.fecha_aceptacion = datetime.datetime.now()
                membresia.ip_peticion = get_client_ip(request)
                membresia.estado = 1
                membresia.fk_institucion = insti
                membresia.fk_usuario = Perfil.objects.get(id=request.session['id_usuario'])
                membresia.save()

                print "registros guardados"  #borrar cuando no lo necesiten mas, no olvidar
                try:
                    membresiaBorrar = Membresia.objects.filter(fk_usuario=request.session['id_usuario'],
                                                               fk_institucion=1).first()
                    membresiaBorrar.delete()
                    print "membresia independiente deleted"  #borrar cuando no lo necesiten mas, no olvidar
                #Error 6, falta retroalimentacion para el usuario.
                except:
                    print "membresia no encontrada"  #borrar cuando no lo necesiten mas, no olvidar
                #Error 6, falta retroalimentacion para el usuario.
                return redirect('/perfilInstitucion')
            else:
                print "peticion ya usada"  #borrar cuando no lo necesiten mas, no olvidar
                #Error 6, falta retroalimentacion para el usuario.
                return redirect('/registro_institucion')
        except:
            print "algo fallo"  #borrar cuando no lo necesiten mas, no olvidar
            #Error 6, falta retroalimentacion para el usuario.
            return redirect('/registro_institucion')


"""
Autor: Angel Guale
Nombre de función: get_client_ip
Parámetros: request
Salida: IP del cliente
Descripción: Esta funcion obtiene la direccion IP del host para hacer uso en
			 el registro de usuarios o instituciones.
"""


def get_client_ip(request): #Error 10, nombre inadecuado de la funcion
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


"""
Autor: Angel Guale
Nombre de función: registro_usuario
Parámetros: request GET o POST
Salida: Formulario de registro usuario
Descripción: Responde con un formulario vacio de registro de usuario o ejecuta el registro de un usuario
"""


def registro_usuario(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/inicioUsuario/')

    else:
        if request.method == 'POST':
            #print request.POST
            #formulario = Form(request.POST)
            username = request.POST['username']  #Error 10, usar palabras en español
            password = request.POST['password1']  #Error 10, usar palabras en español
            nombres = request.POST['nombres']
            apellidos = request.POST['apellidos']
            cedula = request.POST['cedula']
            #cargo=request.POST['cargo']
            telefono = request.POST['telefono']
            #actividad=request.POST['actividad']
            website = request.POST['website']  #Error 10, usar palabras en español
            email = request.POST['email']  #Error 10, usar palabras en español
            pais_selected = request.POST['pais']  #Error 10, usar palabras en español
            ciudad_selected = request.POST['ciudad']  #Error 10, usar palabras en español

            print pais_selected  #borrar luego que no se use mas

            try:
                perfil = Perfil()
                #Error 10, usar palabras en español
                perfil.username = username
                perfil.set_password(password)
                perfil.first_name = nombres
                perfil.last_name = apellidos
                perfil.cedula = cedula
                perfil.web = website
                perfil.email = email

                perfil.fecha_registro = datetime.datetime.now()
                perfil.reputacion = 0
                perfil.estado = 1  #estado 1 es activo
                perfil.telefono = telefono

                pais = Country.objects.get(id=pais_selected)
                ciudad = City.objects.get(id=ciudad_selected)
                perfil.privacidad = 1111
                perfil.fk_ciudad = ciudad
                perfil.fk_pais = pais
                perfil.ip_registro = get_client_ip(request)
                perfil.save()

                membresia = Membresia()
                #Error 10, usar palabras en español
                membresia.es_administrator = 0  #0 para falso
                membresia.cargo = "Independiente"  #independiente no hay cargo
                membresia.descripcion = "Independiente"  #Independiente no hay descripcion
                membresia.fecha_aceptacion = datetime.datetime.now()
                membresia.fecha_peticion = datetime.datetime.now()
                membresia.ip_peticion = get_client_ip(request)
                membresia.estado = 1  #1 es para aceptado
                institucion = Institucion.objects.get(siglas="I")
                membresia.fk_institucion = institucion
                membresia.fk_usuario = perfil
                membresia.save()

                usuario = auth.authenticate(username=username, password=password)
                args = {}

                if usuario is not None:
                    if request.POST.has_key('remember_me'): #Error 10, usar palabras en español
                        request.session.set_expiry(1209600)  # 2 weeks
                    auth.login(request, usuario)
                    request.session['id_usuario'] = usuario.id
                    return HttpResponseRedirect('/perfilUsuario')
                else:
                    return HttpResponseRedirect('/iniciarSesion')

            except:
                #print e.getMessage()
                u_existe = Perfil.objects.get(username=username) #Error 10, usar palabras completas no abreviaturas
                args = {}
                mensaje = "No se pudo crear el usuario"
                if u_existe is not None:
                    args['username'] = "El nombre de usuario ya existe"
                    args.update(csrf(request))
                    paises = Country.objects.all()
                    args['paises'] = paises
                    args['mensaje'] = mensaje
                    return render_to_response('Usuario_Sign-up.html', args)

        else:
            args = {}
            args.update(csrf(request))
            paises = Country.objects.all()
            args['paises'] = paises
            return render_to_response('Usuario_Sign-up.html', args)

"""
Autor: RELLENAR A QUIEN LE CORRESPONDA
Nombre de función:
Parámetros:
Salida:
Descripción:
"""


def index(request): #Error 10, nombre inadecuado de la funcion
    if request.user.is_authenticated():
        return HttpResponseRedirect('/inicioUsuario')
    else:
        return render_to_response('index.html', {})


"""
Autor: Fausto Mora y Roberto Yoncon
Nombre de función: iniciarSesion
Parámetros: request
Salida: hhtp
Descripción: permite el login de un usuario registrado
"""
#usar palabras en español
def iniciarSesion(request): #Error 10, nombre inadecuado de la funcion
    if request.user.is_authenticated():
        return HttpResponseRedirect('/inicioUsuario/')
    else:
        if request.method == 'POST':
            username = request.POST['usernameLogin'] #Error 10, usar palabras en español
            password = request.POST['passwordLogin'] #Error 10, usar palabras en español
            usuario = auth.authenticate(username=username, password=password)
            args = {}

            if usuario is not None:
                if request.POST.has_key('remember_me'):
                    request.session.set_expiry(1209600)  # 2 weeks
                auth.login(request, usuario)
                request.session['id_usuario'] = usuario.id
                return HttpResponseRedirect('/inicioUsuario')
            else:
                error = "Nombre de Usuario o Contraseña Incorrectos"
                args['mensajeErrorIngreso'] = error
                args.update(csrf(request))
                return render_to_response('sign-in.html', args, context_instance=RequestContext(request))
        else:
            print "Error en el request.POST o entro en el enviar email"
    return render_to_response('sign-in.html', {}, context_instance=RequestContext(request))


"""
Autor: Fausto Mora
Nombre de función: cerrarSesion
Parámetros: request
Salida: hhtp
Descripción: hace el logout del usuario y redirecciona a index
"""
#usar palabras en español
def cerrarSesion(request):
    logout(request)
    return redirect('/')


"""
Autor: RELLENAR A QUIEN LE CORRESPONDA
Nombre de función:
Parámetros:
Salida:
Descripción:
"""


@login_required
def editar_usuario(request):
    session = request.session['id_usuario']
    usuario = Perfil.objects.get(id=session)
    args = {}

    if usuario is not None:
        args['usuario'] = usuario
    else:
        args['error'] = "Error al cargar los datos"

    if request.method == 'POST':
        #print request.POST
        nombres = request.POST['nombres']
        apellidos = request.POST['apellidos']
        #cedula=request.POST['cedula']
        #cargo=request.POST['cargo']
        telefono = request.POST['telefono']
        #actividad=request.POST['actividad']
        website = request.POST['website']
        email = request.POST['email']
        try:
            foto = request.FILES['imagen']

        except:
            foto = "noPicture.png"
         #Explicar como funciona el array de privacidad.
        try:
            #privacidadNom=request.POST['PrivacidadNombre']
            #privacidadApe=request.POST['PrivacidadApellido']
            privacidadCed = request.POST['PrivacidadCedula']
            privacidadTel = request.POST['PrivacidadTelefono']
            privacidadWeb = request.POST['PrivacidadWeb']
            privacidadMai = request.POST['PrivacidadMail']
            #if privacidadWeb=="1" and privacidadMai=="1":
            #	privacidadWeb='3'
            #elif privacidadWeb=="0" and privacidadMai=="1":
            #	privacidadWeb='2'
            #privacidad=privacidadNom+privacidadApe+privacidadCed+privacidadTel+privacidadWeb
            privacidad = privacidadCed + privacidadTel + privacidadWeb + privacidadMai

        except:
            privacidad = 1111

        print foto
        perfil = usuario
        perfil.first_name = nombres
        perfil.last_name = apellidos
        #perfil.cedula=cedula
        #perfil.cargo=cargo
        #perfil.actividad=actividad
        perfil.web = website
        perfil.email = email
        #perfil.ciudad=ciudad
        #perfil.fechaNacimiento=fechaNacimiento
        #perfil.areasInteres=areasInteres
        perfil.fecharegistro = datetime.datetime.now()
        perfil.telefono = telefono
        #ubicacion=Ubicacion.objects.get(idubicacion=1)
        #perfil.fkubicacion=ubicacion
        perfil.privacidad = privacidad
        perfil.foto = foto
        perfil.save()

        return HttpResponseRedirect('/perfilUsuario/')
    else:
        args.update(csrf(request))
        return render_to_response('Usuario_Edit-Profile.html', args)


"""
Autor: Roberto Yoncon
Nombre de función: terms
Parámetros: request
Salida: http
Descripción: Muestra la pagina de Terminos y Condiciones del sistema REINET
"""


def terms(request): #Error 10, nombre inadecuado de la funcion
    return render(request, 'terms.html')


"""
Autor: Fausto Mora y Roberto Yoncon
Nombre de función: inicio
Parámetros: request
Salida: http
Descripción: envia la informacion del usuario a una plantilla html
permite ver la pagina inicial de todo usuario logeado
"""


@login_required
def inicio(request):
    session = request.session['id_usuario']
    usuario = Perfil.objects.get(id=session)
    args = {}

    if usuario is not None:
        args['usuario'] = usuario

    else:
        args['error'] = "Error al cargar los datos"

    args.update(csrf(request))
    return render_to_response('Usuario_Home.html', args)


"""
Autor: Fausto Mora, Roberto Yoncon y Angel Guale
Nombre de función: perfilUsuario
Parámetros: request
Salida: http
Descripción: envia la informacion del usuario a una plantilla html
"""


@login_required
def perfilUsuario(request): #Error 10, nombre inadecuado de la funcion
    session = request.session['id_usuario']
    usuario = Perfil.objects.get(id=session)
    args = {}

    if usuario is not None:
        args['usuario'] = usuario
        usuario.estado = 1
        usuario.save()
        perfil = Perfil.objects.get(username=usuario.username)
        args['perfil'] = perfil
        membresia = Membresia.objects.filter(fk_usuario=usuario.id)
        listaInstituciones = []
        for num in range(0, membresia.count()):
            listaInstituciones.append(
                Institucion.objects.get(id_institucion=membresia[num].fk_institucion.id_institucion))
        args['listaInstituciones'] = listaInstituciones
        institucion = Institucion.objects.get(id_institucion=membresia[0].fk_institucion.id_institucion)
        #print institucion
        args['institucion'] = institucion

    else:
        args['error'] = "Error al cargar los datos"
        return HttpResponseRedirect('/iniciarSesion/')

    args.update(csrf(request))
    #args['usuario']=usuario
    return render_to_response('profile_usuario.html', args)


"""
Autores: Ray Montiel y Edinson Sánchez
Nombre de funcion: perfilInstitucion
Entrada: request GET
Salida: Perfil de Institucion
"""


@login_required
def perfilInstitucion(request): #Error 10, nombre inadecuado de la funcion
    session = request.session['id_usuario'] #Error 10, usar palabras en español
    usuario = Perfil.objects.get(id=session)
    args = {}

    if usuario is not None:
        args['usuario'] = usuario
        membresia = Membresia.objects.filter(fk_usuario=usuario.id).first()
        print "sadhas"
        if membresia.es_administrator:
            print "entre"
            print membresia.id_membresia
            institucion = Institucion.objects.get(id_institucion=membresia.fk_institucion.id_institucion)
            #print institucion
            args['institucion'] = institucion
        else:
            print "aca"
            args['error1'] = "Usted no es miembro de ninguna Institucion"

    else:
        args['error'] = "Error al cargar los datos"
        return HttpResponseRedirect('/iniciarSesion/')

    args.update(csrf(request))
    #args['usuario']=usuario
    return render_to_response('profile_institucion.html', args)

"""
Autores: Pedro Iniguez
Nombre de funcion: perfilInstituciones
Entrada: request GET
Salida: Perfil de otra institucion de la que no sea admin
"""


@login_required
def verPerfilInstituciones(request, institucionId): 
	id_institucion = int(institucionId)
	sesion = request.session['id_usuario']
	usuario = Perfil.objects.get(id=sesion)
	args = {}

	if usuario is not None:
		args['usuario'] = usuario
		membresia = Membresia.objects.filter(fk_institucion=id_institucion).first()
		try:
			if membresia.fk_usuario.id == sesion:
				print "redirect"
				return redirect('/perfilInstitucion')
			else:
				institucion = Institucion.objects.get(id_institucion=id_institucion)
				duenho_institucion = Perfil.objects.get(id = membresia.fk_usuario.id)
				args['institucion'] = institucion
				args['duenho'] = duenho_institucion
				print "aca"
		except:
			return redirect('/inicioUsuario')

	else:
		args['error'] = "Error al cargar los datos"
		return HttpResponseRedirect('/iniciarSesion/')

	args.update(csrf(request))
	#args['usuario']=usuario
	return render_to_response('perfil_otra_institucion.html', args)

"""
Autor: Pedro Iniguez
Nombre de funcion: verificarCodigo
Entrada: request POST
Salida: Formulario de registro institucion
Responde con un formulario vacio de registro de institucion
"""


@login_required
def verificarCodigo(request): #Error 10, nombre inadecuado de la funcion
    if request.method == 'POST':
        args = {}
        codigo = request.POST['codigo']
        print codigo
        peticion = Peticion.objects.all().filter(fk_usuario=request.session['id_usuario']).first()
        try:
            print peticion.codigo
            if (peticion.codigo == codigo and peticion.usado == 0):
                paises = Country.objects.all()
                ciudades = City.objects.all().filter(country_id=paises.first().id)
                args['paises'] = paises
                args['ciudades'] = ciudades
                args['codigo'] = peticion.codigo
                args['insti'] = peticion.nombre_institucion
                return render_to_response('institucion_form_response.html', args)
            else:
                return render_to_response('codigo_usado.html')
        except:
            return render_to_response('nocodigo.html')


"""
Autor: Pedro Iniguez
Nombre de funcion: obtenerCiudades
Entrada: request POST
Salida: Opciones de ciudades para el pais seleccionado
Responde con options de ciudades
"""


def obtenerCiudades(request): #Error 10, nombre inadecuado de la funcion
    if request.method == 'POST':
        args = {}
        ciudades = City.objects.all().filter(country_id=request.POST['paisId'])
        args['ciudades'] = ciudades
        print len(ciudades)
        return render_to_response('opcionesCiudades.html', args)


"""
Autor: Kevin Zambrano y Fausto Mora
Nombre de función: suspenderUsuario
Parámetros: request
Salida: http
Descripción: hace la suspension de la cuenta por parte del usuario
"""


@login_required
def suspenderUsuario(request):  #Error 10, nombre inadecuado de la funcion
    usuario = Perfil.objects.get(id=request.session['id_usuario'])
    password_ingresada = request.POST['txt_password_ingresada'] #Error 10, usar palabras en español

    if usuario.check_password(password_ingresada):
        #Cero significa que esta inactivo
        usuario.estado = 0
        usuario.save()
        return cerrarSesion(request)
    else:
        args = {}
        error = "Contraseña Incorrecta"
        args['error'] = error
        args['usuario'] = usuario
        args.update(csrf(request))
        return render(request, 'Usuario_Edit-Profile.html', args)


"""
Autor: Angel Guale
Nombre de funcion: generarCodigo
Entrada: request GET o POST
Salida: Formulario de generarCodigo
Descripción: Genera un codigo para registrar institucion
"""


def generarCodigo(request): #Error 10, nombre inadecuado de la funcion
    if request.method == 'POST':
        username = request.POST['username'] #Error 10, usar palabras en español
        usuario = Perfil.objects.get(username=username)
        codigo = request.POST['codigo']
        nombre_institucion = request.POST['nombre_institucion']
        #creo el registro de peticion
        peticion = Peticion()
        peticion.codigo = codigo
        peticion.nombre_institucion = nombre_institucion
        peticion.usado = 0
        peticion.fk_usuario = usuario
        peticion.save()
        args = {}
        args['mensaje'] = "Codigo Institucion generado"
        return render_to_response('Administrador_generar_codigo.html', args)
    else:
        args = {}
        args.update(csrf(request))

        return render_to_response('Administrador_generar_codigo.html', args)


"""
Autor: Angel Guale
Nombre de funcion: verificar_username
Entrada: request GET o POST
Salida: Formulario de generarCodigo
Descripción: Genera un codigo para registrar institucion
"""


def verificar_username(request):  #Error 10, nombre inadecuado de la funcion
    if request.method == "POST":
        userinput = request.POST['username'] #Error 10, usar palabras en español
        try:
            usuarioquery = Perfil.objects.get(username=userinput) #Error 10, usar palabras en español
        except:
            usuarioquery = None #Error 10, usar palabras en español
        #print "userinput",userinput, "usuarioquery ", usuarioquery
        if usuarioquery is not None: #Error 10, usar palabras en español
            return HttpResponse("usado")
        else:
            return HttpResponse("ok")
    return HttpResponse("no es post")


"""
Autor: RELLENAR A QUIEN LE CORRESPONDA
Nombre de función:
Parámetros:
Salida:
Descripción:
"""

def verCualquierUsuario(request):  #Error 10, nombre inadecuado de la funcion
    username = request.GET.get('u', '') #Error 10, usar palabras en español
    if username != "":
        perfil = Perfil.objects.get(username=username)
        if username is not None:
            args = {}
            args['usuario'] = perfil
            return render_to_response("Usuario_vercualquierPerfil.html", args)


"""
Autor: Fausto Mora
Nombre de funcion: enviarEmailPassword
Entrada: request POST
Salida: Se envia un email 
Descripción: Se envia un email donde el usuario decida, con la Contraseña del usuario 
"""


def enviarEmailPassword(request): #Error 10, nombre inadecuado de la funcion
    destinatario = request.POST['email_recuperacion']
    args = {}
    try:
        usuario = Perfil.objects.get(email=destinatario)
        username = usuario.username.encode('utf-8', errors='ignore') #Error 10, usar palabras en español
        print username
        password = generarPasswordAleatorea() #Error 10, usar palabras en español
        print password
        usuario.set_password(password) #Error 10, usar palabras en español
        usuario.save()

        if destinatario and usuario:
            try:
                html_content = "<p><h2>Hola... Tus datos de acceso son:</h2><br><b>Nombre de Usuario:</b> %s <br><b>Contraseña:</b> %s <br><br><h4>Esta sera tu nueva credencial, se recomienda que la cambies apenas accedas a tu perfil... Gracias¡¡</h4></p>" % (
                    username, password)
                msg = EmailMultiAlternatives('Credenciales de Acceso a Reinet', html_content,
                                             'REINET <from@server.com>', [destinatario])
                msg.attach_alternative(html_content, 'text/html')
                msg.send()
                args['tipo'] = 'success'
                args['mensaje'] = 'Mensaje enviado correctamente'
                print args['mensaje']
                args.update(csrf(request))

            except:
                args['tipo'] = 'error'
                args['mensaje'] = 'Error de envio. Intentelo denuevo'
                print args['mensaje']
                args.update(csrf(request))

        return render(request, 'sign-in.html', args)
    except:
        args['tipo'] = 'info'
        args['mensaje'] = 'No existe usuario asociado a ese email'
        print args['mensaje']
        args.update(csrf(request))
        return render(request, 'sign-in.html', args)


"""
Autor: Fausto Mora
Nombre de funcion: generarPasswordAleatorea
Entrada: -ninguna-
Salida: string
Descripción: genera una cadena de caracteres con letras mayusculas y digitos enteros
de longitud 8 
"""


def generarPasswordAleatorea(): #Error 10, nombre inadecuado de la funcion
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))


"""
Autor: Fausto Mora
Nombre de funcion: csrf_failure
Entrada: request,string
Salida: http
Descripción: maneja el error de csrf
"""


def csrf_failure(request, reason=""):
    return HttpResponseRedirect('/index/')


"""
Autor: Erika Narvaez
Nombre de funcion: modificarPerfilInstitucion
Entrada: request POST
Salida: Redireccion a perfil
"""


@login_required
def modificarPerfilInstitucion(request): #Error 10, nombre inadecuado de la funcion
	usuario_admin = request.user #Error 10, usar palabras en español
	membresia = Membresia.objects.all().filter(fk_usuario=usuario_admin, es_administrator=True).first()
	paises=Country.objects.all()
	ciudades=City.objects.all().filter(country_id = paises.first().id)
	institucion = membresia.fk_institucion
	if request.method=='POST':
		nombre=request.POST.get("nombre")
		siglas=request.POST.get("siglas")
		descripcion=request.POST.get("descripcion")
		mision=request.POST.get("mision")
		web=request.POST.get("webInstitucion")
		recursos=request.POST.get("recursosInstitucion")
		mail=request.POST.get("emailInstitucion")
		telefono = request.POST.get("telefonoInstitucion")


		institucion.nombre=nombre
		institucion.siglas=siglas
		institucion.descripcion=descripcion
		institucion.mision=mision
		institucion.correo=mail
		institucion.web=web
		institucion.recursos_ofrecidos=recursos
		institucion.telefono_contacto=telefono

		institucion.save()

		return HttpResponseRedirect('/perfilInstitucion')
	else:
		#institucion=Institucion.objects.get()

		args ={
			"institucion":institucion,
			"ciudades":ciudades,
			"paises":paises
		}
		args.update(csrf(request))
		return render(request,"institucion_editar.html",args)

