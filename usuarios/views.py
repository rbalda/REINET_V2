# -*- encoding: utf-8 -*-
# Autores: Grupo A - Grupo B
#Nombre del Archivo: views.py
#Codificación: UTF-8
#Descripción: Archivo donde se registran las vistas que atenderan la logica del modulo.
#Notas/Pendientes: Validar que las variables que se obtienen de las sesiones no sean nulas antes de usarlas.

import random
import string

from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt

from .models import *
from usuarios.serializers import InstitucionSerializador, PerfilSerializador, UsuarioSerializador


"""
Autor: Pedro Iñiguez
Nombre de función:  registro_institucion
Parámetros: request GET o POST
Salida: Pagina para el Ingreso de codigo si es GET, debe devolver perfil de la institucion creada.
Descripción: Corresponde a la creacion de la institucion y el anexo con e usuario por medio de membresia,
			 asi como update a la tabla peticion con valor 1 pues se usa el codigo.
"""

@login_required
def registro_institucion(request, codigo):
	if request.method == 'GET':
		codigo_usado = codigo
		try:
			peticion = Peticion.objects.all().filter(fk_usuario=request.session['id_usuario'], codigo = codigo_usado, usado = 0).first()
			print peticion.nombre_institucion
		except:
			print "not gotten"
			return HttpResponseRedirect('/inicioUsuario')

		session = request.session['id_usuario']  #Error 10, usar sesion o algun otro
		usuario = Perfil.objects.get(id=session)
		args = {}
		paises = Country.objects.all()
		ciudades = City.objects.all().filter(country_id=paises.first().id)
		args['insti'] = peticion.nombre_institucion
		args['paises'] = paises
		args['ciudades'] = ciudades
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
				try:
					insti.logo = image #Error 10, usar palabras en español
					insti.save()
				except:
					print "imagen no subida"

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
				request.session['es_admin'] = True
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
				return redirect('/inicioUsuario')
		except:
			print "algo fallo"  #borrar cuando no lo necesiten mas, no olvidar
			#Error 6, falta retroalimentacion para el usuario.
			return redirect('/NotFound')


"""
Autor: Pedro Iniguez
Nombre de funcion: registrarSolicitud
Entrada: request POST
Salida: Registrar peticion
"""
@csrf_exempt
@login_required
def registrarSolicitud(request):
	if request.method == 'POST':
		args = {}
		try:
			peticion = Peticion.objects.get(fk_usuario = request.session['id_usuario'])
			args['msj'] = 'Usted ya ha enviado una solicitud anteriormente. Por favor, revise su correo.'
			args['esAlerta'] = 1
			return render_to_response('respuesta_Solicitud_Institucion.html', args)
		except:
			print "not loaded"

		membresiaOtra = Membresia.objects.filter(fk_usuario = request.session['id_usuario']).exclude(fk_institucion = 1)
		if (len(membresiaOtra)>0):
			print len(membresiaOtra)
			args['msj'] = 'Usted ya pertenece a otra institucion.'
			args['esAlerta'] = 1
			return render_to_response('respuesta_Solicitud_Institucion.html', args)

		try:
			peticion = Peticion.objects.get(nombre_institucion = request.POST['nombre_institucion'])
			args['msj'] = 'Ya existe una INSTITUCION con este nombre'
			args['esAlerta'] = 1
			return render_to_response('respuesta_Solicitud_Institucion.html', args)
		except:
			print "registrando"
			usuario = Perfil.objects.get(id=request.session['id_usuario'])
			peticion = Peticion()
			peticion.codigo = '000000'
			peticion.nombre_institucion = request.POST['nombre_institucion']
			peticion.usado = 0
			peticion.fk_usuario = usuario
			peticion.save()
			args['esAlerta'] = 0
			args['msj'] = 'Se ha enviado su solicitud con exito! Se enviara; un mail de confirmacion a su correo cuando se apruebe la misma.'

		return render_to_response('respuesta_Solicitud_Institucion.html', args)


"""
Autor: Pedro Iniguez
Nombre de funcion: verificar_siglas
Entrada: request POST
Salida: Formulario de verificar siglas
Descripción: envia mensaje si existen o no las siglas ingresadas
"""
@csrf_exempt
def verificar_siglas(request):  
	if request.method == "POST":
		siglas = request.POST['siglas']
		print len(siglas)
		if (len(siglas)<3):
			return HttpResponse("usado")
		if (siglas == "undefined"):
			return HttpResponse("undefined")
		print "hello"
		try:
			institucion = Institucion.objects.get(siglas=siglas) 
		except:
			institucion = None 

		if institucion is not None: #Error 10, usar palabras en español
			return HttpResponse("usado")
		else:
			return HttpResponse("ok")
	return HttpResponse("no es post")

"""
Autor: Pedro Iniguez
Nombre de funcion: verPeticiones
Entrada: request POST
Salida: las peticiones de codigo 000000
"""

@login_required
def verPeticiones(request):
	try:
		args = {}
		args['peticiones'] = Peticion.objects.all().filter(codigo='000000')
		args.update(csrf(request))
		return render_to_response('ver_peticiones.html', args)
	except:
		return HttpResponseRedirect('/NotFound')


"""
Autor: Pedro Iniguez
Nombre de funcion: aceptarPeticiones
Entrada: request POST
Salida: la peticion es aceptada
"""

@login_required
def aceptarPeticiones(request):
	args={}
	try:
		peticion = Peticion.objects.get(id_peticion = request.POST['id_peticion'])
		usuario = Perfil.objects.get(id=peticion.fk_usuario.id)
		destinatario = usuario.email
		codigo = generarPasswordAleatorea()
		peticion.codigo = codigo
		peticion.save()
		html_content = "<p><h2>Hola... puedes crear tu institucion desde el siguiente link: http://www.reinet.org/registro_institucion/" + codigo
		msg = EmailMultiAlternatives('Registra tu institucion en REINET', html_content,
									 'REINET <from@server.com>', [destinatario])
		msg.attach_alternative(html_content, 'text/html')
		msg.send()
		args['esAlerta'] = 0
		args['msj'] = 'Aceptada la institucion ' + peticion.nombre_institucion
		return render_to_response('respuesta_Solicitud_Institucion.html', args)
	except:
		args['esAlerta'] = 1
		args['msj'] = 'Refresque la pagina, error al aceptar ' + peticion.nombre_institucion
		return render_to_response('respuesta_Solicitud_Institucion.html', args)


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

class Email_excepcion(Exception):
	"""Excepción lanzada por errores en las entradas.

	Atributos:
		expresion -- expresión de entrada en la que ocurre el error
		mensaje -- explicación del error
	"""

	def __init__(self, mensaje):
		self.mensaje = mensaje

def registro_usuario(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/inicioUsuario/')

	else:

		if request.method == 'POST':
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
				try:
					usuarioquery = Perfil.objects.filter(email=email).first() #Error 10, usar palabras en español
				except:
					usuarioquery = None #Error 10, usar palabras en español
				#print "userinput",userinput, "usuarioquery ", usuarioquery
				if usuarioquery is not None: #Error 10, usar palabras en español
					print "email repetido"
					raise Email_excepcion("emailrepetido")

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

				try:
					id_institucion=request.POST["institucion"];
					institucion_solicitud=Institucion.objects.get(id_institucion=id_institucion)
					if institucion_solicitud is not None:
						membresia= Membresia()
						membresia.es_administrator=0
						membresia.cargo=""
						membresia.descripcion=""
						membresia.fecha_peticion=datetime.datetime.now()
						membresia.fecha_aceptacion=None
						membresia.ip_peticion=get_client_ip(request)
						membresia.estado=0 #en espera
						membresia.fk_institucion=institucion_solicitud
						membresia.fk_usuario=perfil
						membresia.save()
				except:
					pass

				usuario = auth.authenticate(username=username, password=password)

				if usuario is not None:
					if request.POST.has_key('remember_me'): #Error 10, usar palabras en español
						request.session.set_expiry(1209600)  # 2 weeks
					auth.login(request, usuario)
					request.session['id_usuario'] = usuario.id
					request.session['es_admin'] = False

					print 'buscar error de sixto'
					print usuario.id
					print request.session['id_usuario']
					return HttpResponseRedirect('/perfilUsuario')
				else:
					return HttpResponseRedirect('/iniciarSesion')

			except Exception as e:
				#print e.getMessage()
				args = {}
				mensaje = "No se pudo crear el usuario. Esto pudo deberse a un problema de conexión o a que ingresó datos no válidos"
				args.update(csrf(request))
				paises = Country.objects.all()
				instituciones=Institucion.objects.all()
				args['paises'] = paises
				args['mensaje'] = mensaje
				args['instituciones'] = instituciones
				return render_to_response('Usuario_Sign-up.html', args)

		else:
			args = {}
			args.update(csrf(request))
			paises = Country.objects.all()
			instituciones=Institucion.objects.all()
			args['paises'] = paises
			args['instituciones'] = instituciones
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
				user = Perfil.objects.get(id=usuario.id)
				if user.estado == 1:
					if request.POST.has_key('remember_me'):
						request.session.set_expiry(1209600)  # 2 weeks


					request.session['id_usuario'] = usuario.id
					print 'session es_admin'
					print user
					print user.privacidad
					
					auth.login(request, usuario)
					return HttpResponseRedirect('/inicioUsuario')

				else:
					if user.estado == 0:
						args['mensajeSuspendido']='Su usuario se encuentra suspendido. Contactar con el Administrador para más información'
						args.update(csrf(request))
						return render(request,'sign-in.html',args)
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
Autor: Jose Velez
Nombre de función: editar_contrasena
Parámetros:request
Salida: Redirecciona al perfil de usuario
Descripción: Esta funcion edita la contraseña del usuario y la actualiza en la bases de datos
"""

def editar_contrasena(request):
	session = request.session['id_usuario']
	session_usuario = Perfil.objects.get(id=session)
	args = {}

	if session_usuario is not None:
		args['usuario'] = session_usuario
	else:
		args['error'] = "Error al cargar los datos"

	if request.method == 'POST':
		contrasena_actual = request.POST['passwordActual']
		contrasena_nueva = request.POST['password1']
		contrasena_repetida = request.POST['password2']
		usuario = auth.authenticate(username=session_usuario, password=contrasena_actual)
		if usuario is not None:
			if contrasena_nueva == contrasena_repetida:
				perfil = usuario
				perfil.set_password(contrasena_nueva)
				perfil.save()
				
				if request.POST.has_key('remember_me'): #Error 10, usar palabras en español
						request.session.set_expiry(1209600)  # 2 weeks
				auth.login(request, usuario)
				request.session['id_usuario'] = usuario.id
				request.session['es_admin'] = False
				args['es_admin']=request.session['es_admin']
				args.update(csrf(request))
				mensaje = "La contraseña se cambio exitosamente"
				args['mensaje'] = mensaje
				return render_to_response('editar_contrasena_usuario.html', args)
			else:
				return HttpResponseRedirect('/editar_contrasena/')
		else:
			return HttpResponseRedirect('/editar_contrasena/')
	else:
		user = request.user

		args['es_admin']=request.session['es_admin']
		args.update(csrf(request))
		return render_to_response('editar_contrasena_usuario.html', args)


"""
Autor: Leonel Ramirez - jose Velez
Nombre de funcion: verificar_contrasena
Parámetros: request GET o POST
Salida: Formulario de generarCodigo
Descripción: Genera un codigo para  verificar que la contraseña 
"""

def verificar_contrasena(request):  
	session = request.session['id_usuario']
	usuario = Perfil.objects.get(id=session)
	if request.method == "POST":
		contrasena = request.POST['passwordActual']
		autentificacion = auth.authenticate(username=usuario, password=contrasena)
		
		if autentificacion is not None:
			return HttpResponse("valido")
		else:
			return HttpResponse("invalido")
	return HttpResponse("no es post")



"""
Autor: Jose Velez - Leonel Ramirez
Nombre de función: editar_usuario
Parámetros:request
Salida: Redirecciona al perfil de usuario
Descripción: Esta funcion edita la informacion del usuario y la actualiza en la bases de datos
la opcion privacidad sirve para ocultar datos que no quieres que se muestre a otros usuarios
"""

@login_required
def editar_perfil_usuario(request):
	ID_FOTO = 1
	session = request.session['id_usuario']
	usuario = Perfil.objects.get(id=session)
	membresia = Membresia.objects.filter(fk_usuario_id=session,estado=1).last()
	args = {}

	if usuario is not None:
		args['usuario'] = usuario
		args['membresia'] = membresia
	else:
		args['error'] = "Error al cargar los datos"

	if request.method == 'POST':
		nombres = request.POST['nombres'] 
		apellidos = request.POST['apellidos']
		telefono = request.POST['telefono']
		website = request.POST['website']
		email = request.POST['email']
		try:
			foto = request.FILES['imagen']
		except:
			ID_FOTO = 0 #ID para no guardar foto de noPicture
			foto = "../../media/noPicture.png"
		 #Explicar como funciona el array de privacidad.
		try:
			privacidadCed = request.POST['PrivacidadCedula']
			privacidadTel = request.POST['PrivacidadTelefono']
			privacidadWeb = request.POST['PrivacidadWeb']
			privacidadMai = request.POST['PrivacidadMail']
			privacidad = privacidadCed + privacidadTel + privacidadWeb + privacidadMai

		except:
			privacidad = 1111

		perfil = usuario
		perfil.first_name = nombres
		perfil.last_name = apellidos
		perfil.web = website
		perfil.email = email
		perfil.fecharegistro = datetime.datetime.now()
		perfil.telefono = telefono
		perfil.privacidad = privacidad
		if ID_FOTO != 0:
			perfil.foto = foto
		perfil.save()
		
		if request.POST.has_key('cargo'):
			miembro = membresia
			miembro.cargo = request.POST['cargo']
			miembro.descripcion_cargo = request.POST['descripcion-cargo']
			miembro.save()

		return HttpResponseRedirect('/perfilUsuario/')
	else:
		user = request.user
		args['es_admin']=request.session['es_admin']
		args.update(csrf(request))
		return render_to_response('editar_perfil_usuario.html', args)


"""
Autor: Roberto Yoncon
Nombre de función: terminosCondiciones
Parámetros: request
Salida: http
Descripción: Muestra la pagina de Terminos y Condiciones del sistema REINET
"""

def ver_terminos_condiciones(request):
	args={}
	if request.user.is_authenticated():
		args['base_template']='Usuario_Home.html'
		args['usuario']=request.user
	else:
		args['base_template']='index.html'

	print args['base_template']

	args['es_admin']=request.session['es_admin']
	args.update(csrf(request))
	return render(request, 'terminos_y_condiciones.html',args)


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
	print session

	usuario = Perfil.objects.get(id=session)
	args = {}

	if usuario is not None:
		args['usuario'] = usuario
		user = request.user

		#Valida si el usuario tiene una institucion a su cargo o es administrador.
		membresia = Membresia.objects.filter(es_administrator=1,fk_usuario=user).exclude(fk_institucion=1).first()
		print 'usuario' 
		print user.id
		print 'la membresia'
		print membresia
		#Intenta obtener si tiene alguna peticion pendiente.
		peticion_pendiente = Peticion.objects.filter(fk_usuario=user).count()
		print 'peticion_pendiente'
		print peticion_pendiente
		#Si tiene alguna membresia.
		if membresia is not None :
			#Si es administrador de alguna institucion o tiene una peticion pendiente.
			if membresia.es_administrator or peticion_pendiente==0:
				request.session['es_admin'] = True
				institucion = Institucion.objects.get(id_institucion=membresia.fk_institucion.id_institucion)
				request.session['institucion_nombre']=institucion.nombre
			else:
				request.session['es_admin'] = False
				request.session['institucion_nombre']=None
		else:
			request.session['es_admin'] = False	
			request.session['institucion_nombre']=None

	else:

		args['error'] = "Error al cargar los datos"

	args['es_admin']=request.session['es_admin']
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
	print 'session es_admin'
	print request.session['es_admin']
	session = request.session['id_usuario']
	usuario = Perfil.objects.get(id=session)
	args = {}

	if usuario is not None:
		args['usuario'] = usuario
		#cambiar esto, esto solo debe poder hacerlo el administrador
		usuario.estado = 1
		usuario.save()
		perfil = Perfil.objects.get(username=usuario.username)
		args['perfil'] = perfil
		membresias = Membresia.objects.filter(fk_usuario=usuario.id)


		membresia = membresias.filter(estado=1).exclude(fk_institucion=1).first()
		if membresia is not None:
			try:
				institucion = Institucion.objects.get(id_institucion=membresia.fk_institucion.id_institucion)
				args['institucion'] = institucion
			except ObjectDoesNotExist:
				institucion = "Independiente"
				args['institucion'] = institucion
		else:
			institucion = "Independiente"
			args['institucion'] = institucion

	else:
		args['error'] = "Error al cargar los datos"
		return HttpResponseRedirect('/iniciarSesion/')

	args.update(csrf(request))
	args['es_admin']=request.session['es_admin']
	return render_to_response('profile_usuario.html', args)


"""
Autores: Ray Montiel, Edinson Sánchez y Roberto Yoncon
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
		#Guardo en la variable de sesion a usuario.
		args['usuario'] = usuario
		#Saco la membresia de la que soy administrador, y me aseguro que no sea la institucion independiente.
		membresia = Membresia.objects.filter(es_administrator=1,fk_usuario=usuario.id).exclude(fk_institucion=1).first()
		#Si existe un registro es por que soy administrador de una institucion.
		if membresia is not None :
			if membresia.es_administrator :
				print membresia.id_membresia
				institucion = Institucion.objects.get(id_institucion=membresia.fk_institucion.id_institucion)
				numMiembros = Membresia.objects.filter(fk_institucion_id=institucion.id_institucion).values_list('fk_usuario_id', flat=True).distinct().count()
				args['institucion'] = institucion
				args['numMiembros'] = numMiembros
				request.session['institucion_id'] = institucion.id_institucion
				request.session['es_admin'] = True
				request.session['institucion_nombre'] = institucion.nombre
		#Sino, simplemente no tengo ninguna institucion a mi cargo y regreso a mi perfil
		else:
			args['error1'] = "Usted no es miembro de ninguna Institucion"
			return HttpResponseRedirect('/perfilUsuario/')


	else:
		args['error'] = "Error al cargar los datos"
		return HttpResponseRedirect('/NotFound/')

	args.update(csrf(request))
	#args['usuario']=usuario
	args['es_admin']=request.session['es_admin']
	args['institucion_nombre'] = request.session['institucion_nombre']
	return render_to_response('profile_institucion.html', args)


"""
Autores: Pedro Iniguez
Nombre de funcion: perfilInstituciones
Entrada: request GET
Salida: Perfil de otra institucion de la que no sea admin
UltimaModificacion: Fausto Mora - se le agrego un argumento para saber si la institucion
a la que queria acceder es la misma a la que pertenece
"""

@login_required
def verPerfilInstituciones(request, institucionId):
	id_institucion = institucionId
	sesion = request.session['id_usuario']
	usuario = Perfil.objects.get(id=sesion)
	args = {}

	if usuario is not None:
		args['usuario'] = usuario
		membresia = Membresia.objects.filter(fk_institucion=id_institucion,es_administrator=1).first()
		try:
			if membresia.fk_usuario.id == sesion:
				print "redirect"
				return redirect('/perfilInstitucion')
			else:
				institucion = Institucion.objects.get(id_institucion=id_institucion)
				numMiembros = Membresia.objects.filter(fk_institucion_id=institucion.id_institucion).values_list('fk_usuario_id', flat=True).distinct().count()
				duenho_institucion = Perfil.objects.get(id = membresia.fk_usuario.id)

				args['numMiembros'] = numMiembros

				# aqui buscaqueremos si es afiliado a la misma institucion que desea buscar
				institucion_afiliada = Membresia.objects.filter(fk_usuario=sesion,estado=1).exclude(fk_institucion=1).first()
				if institucion_afiliada:
					args['es_afiliado']=True
					print institucion_afiliada.fk_institucion.nombre

					print 'es la misma institucion'
					print institucion_afiliada.fk_institucion.nombre
					print institucion.nombre
					args['misma_institucion'] = institucion_afiliada.fk_institucion.id_institucion == institucion.id_institucion
					print args['misma_institucion']
				else:
					args['es_afiliado']=False

				args['institucion'] = institucion
				args['duenho'] = duenho_institucion
		except:
			return redirect('/NotFound')

	else:
		args['error'] = "Error al cargar los datos"
		return HttpResponseRedirect('/iniciarSesion/')

	args.update(csrf(request))
	#args['usuario']=usuario
	args['es_admin']=request.session['es_admin']
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
		user = request.user
		error = "Contraseña Incorrecta"
		args['error'] = error
		args['usuario'] = usuario
		args.update(csrf(request))
		return render(request, 'editar_perfil_usuario.html', args)



"""
Autor: Angel Guale
Nombre de funcion: generar_codigo
Entrada: request GET o POST
Salida: Formulario de generar_codigo
Descripción: Genera un codigo para registrar institucion
"""

def generar_codigo(request): #Error 10, nombre inadecuado de la funcion
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
		args['mensaje'] = "Codigo Institución Generado"
		return render_to_response('generar_codigo.html', args)
	else:
		args = {}
		args.update(csrf(request))

		return render_to_response('generar_codigo.html', args)


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
Autor: Angel Guale
Nombre de funcion: verificar_username
Entrada: request GET o POST
Salida: Formulario de generarCodigo
Descripción: Genera un codigo para registrar institucion
"""

def verificar_cedula(request):  #Error 10, nombre inadecuado de la funcion
	if request.method == "POST":
		cedula_input = request.POST['cedula'] #Error 10, usar palabras en español
		try:
			usuarioquery = Perfil.objects.get(cedula=cedula_input) #Error 10, usar palabras en español
		except:
			usuarioquery = None #Error 10, usar palabras en español
		#print "userinput",userinput, "usuarioquery ", usuarioquery
		if usuarioquery is not None: #Error 10, usar palabras en español
			return HttpResponse("usado")
		else:
			return HttpResponse("ok")
	return HttpResponse("no es post")


"""
Autor: Angel Guale
Nombre de funcion: verificar_username
Entrada: request GET o POST
Salida: Formulario de generarCodigo
Descripción: Genera un codigo para registrar institucion
"""

def verificar_email(request):  #Error 10, nombre inadecuado de la funcion
	if request.method == "POST":
		email_input = request.POST['email'] #Error 10, usar palabras en español
		try:
			usuarioquery = Perfil.objects.filter(email=email_input).first() #Error 10, usar palabras en español
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

@login_required
def verCualquierUsuario(request, username):  #Error 10, nombre inadecuado de la funcion
	usuario = Perfil.objects.get(id=request.session['id_usuario'])
	if username != "":
		try:
			perfil = Perfil.objects.get(username=username)
			print perfil.username
			print perfil.first_name
			print perfil.last_name
			if username is not None:
				args = {}
				args['usuario'] = usuario
				print usuario
				args['usuario_otro'] = perfil
				print perfil

				# obtener la membresia del usuario_otro
				membresia = Membresia.objects.get(fk_usuario=perfil.id,estado=1)
				print membresia.id_membresia
				institucion = Institucion.objects.get(id_institucion=membresia.fk_institucion.id_institucion)
				args['institucion'] = institucion
				print institucion.nombre
				args.update(csrf(request))
				args['es_admin']=request.session['es_admin']
				return render(request,"Usuario_vercualquierPerfil.html", args)
		except:
			return HttpResponseRedirect('/NotFound')
	else:
		return HttpResponseRedirect('/NotFound')


"""
Autor: Fausto Mora y Roberto Yoncon
Nombre de funcion: enviarEmailPassword
Entrada: request POST
Salida: Se envia un email 
Descripción: Se envia un email donde el usuario decida, con la Contraseña del usuario 
"""

def enviarEmailPassword(request): #Error 10, nombre inadecuado de la funcion
	try:
		destinatario = request.POST['email_recuperacion']
		args = {}
		try:
			usuario = User.objects.get(email=destinatario)
			username = usuario.username.encode('utf-8', errors='ignore') #Error 10, usar palabras en español

			codigo = generarPasswordAleatorea()
			link='http://localhost:8000/recuperarPassword/'+ codigo
			# link cuando este en realease -  no se si funcionara - no estoy seguro del puerto tampoco
			#link='http://201.183.227.87:13306/recuperarPassword/'
			
			if codigo:
				peticion = Peticion()
				peticion.nombre_institucion = 'tipo-recuperar-password'
				peticion.codigo = codigo
				peticion.usado = False
				peticion.fk_usuario = usuario
				peticion.save()

				if destinatario and usuario:
					try:
						html_content = "<p><h2>Hola... </h2><h4>Se te ha enviado este email para restablecer tu credencial de acceso a Reinet.</h4><br><h4> Tu nombre de Usuario es:</b> %s .Para resetear tu contraseña dale click al siguiente link: </h4><a href=%s>http://www.reinet.org/recuperarPassword/%s</a> <br><h4>Muchas gracias por usar nuestro sitio!</h4><br><h4>El equipo de Reinet</h4></p>" % (
							username,link,codigo)
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

		except User.DoesNotExist:
			args['tipo'] = 'info'
			args['mensaje'] = 'No existe usuario asociado a ese email'
			print args['mensaje']
			args.update(csrf(request))
			return render(request, 'sign-in.html', args)
	except:
		print 'error'
		return redirect('/')


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
Autor: Fausto Mora
Nombre de funcion: recuperarPassword
Entrada: request POST
Salida: Redireccion inicio usuario
Descripción: Esta funcion permite el cambio de contraseña cuando se 
recupera la contraseña desde un correo enviado por mail, mediante redireccion
"""

def recuperarPassword(request,codigo):
	codigo_password = codigo
	print codigo
	if codigo_password:
		try:
			# usare la tabla peticion para crear el nexo con el usuario a la hora de cambiar contraseña
			peticion = Peticion.objects.get(codigo=codigo_password)
			# validacion de la tabla peticiones para poder resetear contraseña
			if not peticion.usado and peticion.nombre_institucion == 'tipo-recuperar-password':

				usuario = User.objects.get(id=peticion.fk_usuario.id)
				args={}
				if request.method == 'POST':
					pass1 = request.POST['passwordSet1']
					pass2 = request.POST['passwordSet2']
					if pass1 == pass2:
						usuario.set_password(pass1)
						usuario.save()

						peticion.usado = True
						peticion.save()

						usuario = auth.authenticate(username=usuario.username, password=pass1)
						auth.login(request, usuario)
						request.session['id_usuario'] = usuario.id
						return HttpResponseRedirect('/inicioUsuario/')
					else:
						print 'pass no coincidieron'
						return redirect('/NotFound/')

				args['codigo']=codigo_password
				args.update(csrf(request))
				return render(request,'recuperar_password.html',args)
			else:
				print 'peticion usada o diferente peticion'
				return redirect('/NotFound/')

		except Peticion.DoesNotExist:
			print 'peticion no existe'
			return redirect('/NotFound/')
		except User.DoesNotExist:
			print 'usuario no existe'
			return redirect('/NotFound/')
	else:
		print 'codigo es nulo'
		return redirect('/NotFound/')

"""
Autor: Erika Narvaez
Nombre de funcion: modificarPerfilInstitucion
Entrada: request POST
Salida: Redireccion a perfil
"""

@login_required
def modificarPerfilInstitucion(request): #Error 10, nombre inadecuado de la funcion
	try:
		usuario_admin = request.user #Error 10, usar palabras en español
		membresia = Membresia.objects.all().filter(fk_usuario=usuario_admin, es_administrator=True).first()
		paises=Country.objects.all()
		ciudades=City.objects.all().filter(country_id = paises.first().id)
		institucion = membresia.fk_institucion

		idLogo = 1 # Id del logo
		if request.method=='POST':
			nombre=request.POST.get("nombre")
			siglas=request.POST.get("siglas")
			descripcion=request.POST.get("descripcion")
			mision=request.POST.get("mision")
			web=request.POST.get("webInstitucion")
			recursos=request.POST.get("recursosofrecidos")
			mail=request.POST.get("emailInstitucion")
			telefono = request.POST.get("telefonoInstitucion")
			try:
				image = request.FILES['logo']
			except:
				idLogo = 0 #ID para no guardar logo noPicture.png
				image = "../../media/noPicture.png"

			institucion.nombre=nombre
			institucion.siglas=siglas
			institucion.descripcion=descripcion
			institucion.mision=mision
			institucion.correo=mail
			institucion.web=web
			institucion.recursos_ofrecidos=recursos
			institucion.telefono_contacto=telefono
			if idLogo != 0:
				institucion.logo = image
			institucion.save()

			return HttpResponseRedirect('/perfilInstitucion')
		else:
			#institucion=Institucion.objects.get()

			args ={
				"usuario":usuario_admin,
				"institucion":institucion,
				"ciudades":ciudades,
				"paises":paises,
			}
			args.update(csrf(request))
			args['es_admin']=request.session['es_admin']
			args['institucion_nombre'] = request.session['institucion_nombre']
			return render(request,"institucion_editar.html",args)
	except:
		return redirect('/')


"""
Autor: Rene Balda
Nombre de funcion: Busqueda de Institucion y personas
Entrada: request
Salida: Redireccion bandeja de entrada
Descripción: Esta funcion permite visualizar los mensajes
que un usuario tiene en su bandeja de entrada
"""
class InstitucionBusqueda(ListAPIView):
	queryset = Institucion.objects.all()
	serializer_class = InstitucionSerializador
	permission_classes = (IsAuthenticated,)

	def list(self, request):
		busqueda = self.request.query_params.get('busqueda',None)
		queryset = []

		if busqueda is not None and busqueda!='':
			queryset = self.get_queryset().filter(siglas__icontains=busqueda)
			queryset = queryset|self.get_queryset().filter(nombre__icontains=busqueda)
		lista_serializada = self.get_serializer_class()(queryset[:3],many=True)
		return Response(lista_serializada.data)

class PerfilBusqueda(ListAPIView):
	queryset = Perfil.objects.all()
	serializer_class = PerfilSerializador
	permission_classes = (IsAuthenticated,)

	def list(self, request):
		busqueda = self.request.query_params.get('busqueda',None)
		queryset = []

		if busqueda is not None and busqueda!='':
			queryset = self.get_queryset().filter(first_name__icontains=busqueda)
			queryset = queryset | self.get_queryset().filter(last_name__icontains=busqueda)
		lista_serializada = self.get_serializer_class()(queryset[:3],many=True)
		return Response(lista_serializada.data)

class NumeroMensajesNoLeidos(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self,request,*args,**kwargs):
		no_leidos = Mensaje.objects.filter(fk_receptor=request.user,leido=False)
		total = len(no_leidos)
		response = Response(total,status=status.HTTP_200_OK)
		return response


class NumeroNotificacionesNoLeidos(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self,request,*args,**kwargs):
		no_leidos = Notificacion.objects.filter(destinatario_notificacion=request.user,estado_notificacion=False)
		total = len(no_leidos)
		response = Response(total,status=status.HTTP_200_OK)
		return response


"""
Autor: Ray Montiel
Nombre de funcion: verMensajes
Entrada: request
Salida: Redireccion bandeja de entrada
Descripción: Esta funcion permite visualizar los mensajes
que un usuario tiene en su bandeja de entrada
UltimaModificacion: Fausto Mora - 4/7/15  
"""

@login_required
def ver_bandeja_entrada(request):
	sesion = request.session['id_usuario']
	usuario=User.objects.get(id=sesion)

	try:
		mensajes = Mensaje.objects.all().filter(fk_receptor=request.session['id_usuario'],visible_receptor = 1).exclude(tipo_mensaje='institucion-institucion').exclude(tipo_mensaje='usuario-institucion')
	except:
		mensajes= None
	mensajes = mensajes.order_by('-fecha_de_envio')

	paginacion = Paginator(mensajes, 5)
	print paginacion.count
	try:
		page=int(request.GET.get('page', '1'))
	except ValueError:
		page=1

	try:
		msjs = paginacion.page(page)
	except (EmptyPage, InvalidPage):
		msjs = paginacion.page(paginacion.num_pages)

	args={}
	args['usuario'] = usuario
	args['mensajes'] = mensajes
	args['msjs'] = msjs
	args['range']=range(len(mensajes))
	args['es_admin']=request.session['es_admin']

	for m in mensajes:
		print m.imgEm
	return render_to_response('bandeja_de_entrada.html',args)


"""
Autor: Ray Montiel & Kevin Zambrano
Nombre de funcion: verMensajes
Entrada: request
Salida: Redireccion bandeja de entrada de institucion
Descripción: Esta funcion permite visualizar los mensajes
que un usuario tiene en su bandeja de entrada de institucion
UltimaModificacion: Fausto Mora - 4/7/15  
"""

@login_required
def ver_bandeja_entrada_institucion(request):
	if request.session['es_admin']:
		sesion = request.session['id_usuario']
		usuario=User.objects.get(id=sesion)

		
		mensajes = Mensaje.objects.all().filter(fk_receptor=request.session['id_usuario'],visible_receptor = 1).exclude(tipo_mensaje='institucion-usuario').exclude(tipo_mensaje='usuario-usuario')
		print mensajes
		mensajes = mensajes.order_by('-fecha_de_envio')
		paginacion = Paginator(mensajes, 5)

		try:
			page=int(request.GET.get('page', '1'))
		except ValueError:
			page=1

		try:
			msjs = paginacion.page(page)
		except (EmptyPage, InvalidPage):
			msjs = paginacion.page(paginacion.num_pages)

		args={}
		args['usuario'] = usuario
		args['mensajes'] = mensajes
		args['msjs'] = msjs
		args['range']=range(len(mensajes))
		args['es_admin']=request.session['es_admin']
		args['institucion_nombre'] = request.session['institucion_nombre']
		args.update(csrf(request))

		for m in mensajes:
			print m.imgEm
		return render_to_response('bandeja_de_entrada_institucion.html',args)
	else:
		return redirect('/')


"""
Autor: Ray Montiel
Nombre de funcion: enviarMensaje
Entrada: request POST
Salida: Redireccion bandeja de entrada
Descripción: Esta funcion permite visualizar los mensajes
que un usuario tiene en su bandeja de entrada
Ultima Modificacion: Rolando Sornoza - Se realizo la implementacion de añadir mensajes de retroalimentacion
y se valido cosas que estaban mal validadas.
"""

@login_required
def enviarMensaje(request):
	sesion=request.session['id_usuario']
	usuario=User.objects.get(id=sesion)
	args = {}
	if request.method=='POST':
		print "envio de mensajes desde usuario"
		destinatario = request.POST['destinatario']
		asunto = request.POST['asunto']
		texto_mensaje = request.POST['mensaje']
		emisor=User.objects.get(id=sesion)

		if destinatario == emisor.username:
			args['RetroMensaje'] = 'El mensaje te lo estas enviando tu tarado'
			args['alertaMensaje'] = 1
			return render_to_response("respuesta_mensaje.html",args)
		else:
			try:
				receptor_aux = User.objects.get(username=destinatario)
				receptor=receptor_aux
				tipo_mensaje = 'usuario-usuario'
			except User.DoesNotExist:
				try:
					receptor_aux = Institucion.objects.get(siglas=destinatario)
					membresia_institucion = Membresia.objects.get(fk_institucion=receptor_aux,es_administrator=1)
					receptor = User.objects.get(username=membresia_institucion.fk_usuario.username)
					tipo_mensaje = 'usuario-institucion'
				except Institucion.DoesNotExist:
					args['RetroMensaje'] = 'El usuario no existe'
					args['alertaMensaje'] = 1
					return render_to_response("respuesta_mensaje.html",args)
			try:
				if receptor is not None:
					mensajes = Mensaje()
					mensajes.fk_emisor = emisor
					mensajes.fk_receptor = receptor
					mensajes.asunto = asunto
					mensajes.tipo_mensaje = tipo_mensaje
					mensajes.mensaje= texto_mensaje
					mensajes.fecha_de_envio=datetime.datetime.now()
					mensajes.save()
					args['RetroMensaje'] = 'El mensaje ha sido enviado correctamente Bronza'
					args['alertaMensaje'] = 0
					return render_to_response("respuesta_mensaje.html",args)
				else:
					args['RetroMensaje'] = 'Usuario Invalido Bronza'
					args['alertaMensaje'] = 1
					return render_to_response("respuesta_mensaje.html",args)
			except Exception as e:
				args['RetroMensaje'] = 'Algo Salio Mal, lloremos juntos.'
				args['alertaMensaje'] = 1
				return render_to_response("respuesta_mensaje.html",args)
	else:
		args['usuario']=usuario
		args['es_admin']=request.session['es_admin']
		args.update(csrf(request))
		return render(request,'enviar_mensaje.html',args)

"""
Autor: Ray Montiel & Kevin Zambrano
Nombre de funcion: enviarMensaje
Entrada: request POST
Salida: Redireccion bandeja de entrada de institucion
Descripción: Esta funcion permite visualizar los mensajes
que un usuario administrador de una institucion tiene en su bandeja de entrada
UltimaModificacion: Fausto Mora - 4/7/15  
"""

@login_required
def enviarMensajeInstitucion(request):
	if request.session['es_admin']:
		print 'dentro de enviar mensaje institucion'
		sesion=request.session['id_usuario']
		usuario=User.objects.get(id=sesion)
		args = {}
		if request.method=='POST':
			print "envio de mensajes desde institucion"
			destinatario = request.POST['destinatario']
			asunto = request.POST['asunto']
			texto_mensaje = request.POST['mensaje']
			emisor=User.objects.get(id=sesion)
			print destinatario
			print emisor
			print texto_mensaje

			if destinatario == emisor:
				args['mensaje_alerta']="No te puedes auto-enviar un mensaje"
			else:

				# averiguamos quien es el destinatario.... si es inst o usuario
				print 'averiguaremos el destinatario'
				try:
					print 'sera usuario?'
					receptor_aux = User.objects.get(username=destinatario)
					receptor=receptor_aux
					print receptor_aux
					tipo_mensaje = 'institucion-usuario'
				except User.DoesNotExist:
					print 'No es usuario'
					print 'sera institucion?'
					receptor_aux = Institucion.objects.get(siglas=destinatario)
					membresia_institucion = Membresia.objects.get(fk_institucion=receptor_aux,es_administrator=1)
					receptor = User.objects.get(username=membresia_institucion.fk_usuario.username)
					print receptor_aux
					tipo_mensaje = 'institucion-institucion'
				except Institucion.DoesNotExist:
					print 'No es institucion'
					print 'hay un grave error aqui'

				try:

					if receptor is not None:
						mensajes = Mensaje()
						mensajes.fk_emisor = emisor
						mensajes.fk_receptor = receptor
						mensajes.asunto = asunto
						mensajes.tipo_mensaje = tipo_mensaje
						mensajes.mensaje= texto_mensaje
						mensajes.fecha_de_envio=datetime.datetime.now()
						mensajes.save()
						return HttpResponseRedirect('/mensajesEnviadosInstitucion/')
					else:
						print "usuariou invalido1"
						return HttpResponseRedirect('/enviarMensajeInstitucion/')
				except Exception as e:
					print "erro al guardar mensaje"
					print e
					return HttpResponseRedirect('/NotFound/')
		else:
			print "porque D: esto es GET"
			args['usuario']=usuario
			args['es_admin']=request.session['es_admin']
			args['institucion_nombre'] = request.session['institucion_nombre']
			args.update(csrf(request))
			return render(request,'enviar_mensaje_institucion.html',args)
	else:
		return redirect('/')


"""
Autor: Ray Montiel
Nombre de funcion: verMensaje
Entrada: request POST
Salida: Redireccion mensaje recibido
Descripción: Esta funcion permite visualizar los mensajes
detalladamente
"""

@login_required
def verMensaje(request):
	sesion=request.session['id_usuario']
	usuario=User.objects.get(id=sesion)
	args = {}
	try:
		idM = int(request.GET.get('q', ''))
		msj=Mensaje.objects.get(id_mensaje = idM)
		print "mensaje",msj.id_mensaje
		print msj.leido
		if msj.fk_receptor == usuario:
			msj.leido = True
			msj.save()
			print msj.leido
			usuario_emisor=msj.fk_emisor
			emisor = Perfil.objects.get(username= usuario_emisor.username)
			receptor = Perfil.objects.get(username = usuario.username)
			args['msj']=msj
			args['usuario_emisor'] = usuario_emisor
			args['emisor']=emisor
			args['receptor']=receptor
			args['usuario']=usuario
			args['es_admin']=request.session['es_admin']
			return render_to_response('ver_mensaje.html',args)
		else:
			print "mi usuario es", msj.fk_receptor, "y tengo", usuario
			return HttpResponseRedirect("/BandejaDeEntrada/")
	except:
		return HttpResponseRedirect("/BandejaDeEntrada/")

"""
Autor: Ray Montiel
Nombre de funcion: verMensaje
Entrada: request POST
Salida: Redireccion mensaje recibido
Descripción: Esta funcion permite visualizar los mensajes
detalladamente
"""

@login_required
def verMensajeEnviado(request):
	sesion=request.session['id_usuario']
	usuario=User.objects.get(id=sesion)
	args = {}
	try:
		idM = int(request.GET.get('q', ''))
		msj=Mensaje.objects.get(id_mensaje = idM)
		print "mensaje",msj.id_mensaje
		print msj.leido
		print msj.fk_emisor
		print usuario
		if msj.fk_emisor == usuario:
			msj.leido = True
			msj.save()
			print msj.leido
			usuario_receptor=msj.fk_receptor
			receptor = Perfil.objects.get(username= usuario_receptor.username)
			emisor = Perfil.objects.get(username = usuario.username)
			args['msj']=msj
			args['usuario_receptor'] = usuario_receptor
			args['emisor']=emisor
			args['receptor']=receptor
			args['usuario']=usuario
			args['es_admin']=request.session['es_admin']
			return render_to_response('ver_mensaje_enviado.html',args)
		else:
			print "porque no entre si mi usuario es", msj.fk_emisor.id, usuario.id
			return HttpResponseRedirect("/mensajesEnviados/")
	except:
		return HttpResponseRedirect("/mensajesEnviados/")
"""
Autor: Fausto Mora
Nombre de funcion: verMensajeInstitucion
Entrada: request POST
Salida: Redireccion mensaje recibido
Descripción: Esta funcion permite visualizar los mensajes
detalladamente desde el buzon de administrador de institucion
"""

@login_required
def verMensajeInstitucion(request):
	if request.session['es_admin']:
		sesion=request.session['id_usuario']
		usuario=User.objects.get(id=sesion)
		args = {}
		#try:
		idM = int(request.GET.get('q', ''))
		msj=Mensaje.objects.get(id_mensaje = idM)
		print "mensaje",msj.id_mensaje
		print msj.leido
		msj.leido = True
		msj.save()
		print msj.leido
		usuario_emisor=msj.fk_emisor
		emisor = Perfil.objects.get(username= usuario_emisor.username)
		receptor = Perfil.objects.get(username = usuario.username)
		args['msj']=msj
		args['usuario_emisor'] = usuario_emisor
		args['emisor']=emisor
		args['receptor']=receptor
		args['usuario']=usuario
		args['es_admin']=request.session['es_admin']
		args['institucion_nombre'] = request.session['institucion_nombre']
		args.update(csrf(request))
		return render_to_response('ver_mensaje_institucion.html',args)
	else:
		return redirect('/')	

"""
Autor: Fausto Mora
Nombre de funcion: verMensajeEnviadoInstitucion
Entrada: request POST
Salida: Redireccion mensaje recibido
Descripción: Esta funcion permite visualizar los mensajes
detalladamente desde el buzon de administrador de institucion
"""

@login_required
def verMensajeEnviadoInstitucion(request):
	if request.session['es_admin']:
		sesion=request.session['id_usuario']
		usuario=User.objects.get(id=sesion)
		args = {}
		try:
			idM = int(request.GET.get('q', ''))
			msj=Mensaje.objects.get(id_mensaje = idM)
			print "mensaje",msj.id_mensaje
			print msj.leido
			msj.leido = True
			msj.save()
			print msj.leido
			usuario_receptor=msj.fk_receptor
			receptor = Perfil.objects.get(username= usuario_receptor.username)
			emisor = Perfil.objects.get(username = usuario.username)
			args['msj']=msj
			args['usuario_receptor'] = usuario_receptor
			args['emisor']=emisor
			args['receptor']=receptor
			args['usuario']=usuario
			args['es_admin']=request.session['es_admin']
			args['institucion_nombre'] = request.session['institucion_nombre']
			args.update(csrf(request))
			return render_to_response('ver_mensaje_enviado_institucion.html',args)
		except:
			return HttpResponseRedirect("/mensajesEnviadosInstitucion/")
	else:
		return redirect('/')

"""
Autor: Ray Montiel
Nombre de funcion: mensajesEnviados
Entrada: request POST
Salida: Muestra los mensajes enviados
Descripción: Esta funcion permite visualizar los mensajes
enviados a otros usuarios
UltimaModificacion: Fausto Mora - 4/7/15  
"""

@login_required
def mensajesEnviados(request):
	sesion = request.session['id_usuario']
	usuario=User.objects.get(id=sesion)


	mensajes = Mensaje.objects.all().filter(fk_emisor=request.session['id_usuario'],visible_emisor = 1).exclude(tipo_mensaje='institucion-usuario').exclude(tipo_mensaje='institucion-institucion')
	print mensajes
	mensajes = mensajes.order_by('-fecha_de_envio')
	paginacion = Paginator(mensajes, 5)

	try:
		page=int(request.GET.get('page', '1'))
	except ValueError:
		page=1

	try:
		msjs = paginacion.page(page)
	except (EmptyPage, InvalidPage):
		msjs = paginacion.page(paginacion.num_pages)

	args={}
	args['usuario']=usuario
	args['msjs']=msjs
	args['mensajes']=mensajes
	args['es_admin']=request.session['es_admin']
	return render_to_response('mensajes_enviados.html',args)

"""
Autor: Ray Montiel & Kevin Zambrano
Nombre de funcion: mensajesEnviados
Entrada: request POST
Salida: Muestra los mensajes enviados de una institucion
Descripción: Esta funcion permite visualizar los mensajes
enviados a otros usuarios
"""

@login_required
def mensajesEnviadosInstitucion(request):
	if request.session['es_admin']:
		sesion = request.session['id_usuario']
		usuario=User.objects.get(id=sesion)


		mensajes = Mensaje.objects.all().filter(fk_emisor=request.session['id_usuario'],visible_emisor = 1).exclude(tipo_mensaje='usuario-usuario').exclude(tipo_mensaje='usuario-institucion')
		print mensajes
		mensajes = mensajes.order_by('-fecha_de_envio')
		paginacion = Paginator(mensajes, 5)
		try:
			page=int(request.GET.get('page', '1'))
		except ValueError:
			page=1

		try:
			msjs = paginacion.page(page)
		except (EmptyPage, InvalidPage):
			msjs = paginacion.page(paginacion.num_pages)

		args={}
		args['usuario']=usuario
		args['msjs']=msjs
		args['mensajes']=mensajes
		args['es_admin']=request.session['es_admin']
		args['institucion_nombre'] = request.session['institucion_nombre']
		args.update(csrf(request))
		return render_to_response('mensajes_enviados_institucion.html',args)
	else:
		return redirect('/')

"""
Autor: Rolando Sornoza, Roberto Yoncon
Nombre de la funcion: mostrar_miembros_institucion
Entrada:
Salida: Muestra los miembros de una institución
Descripción:Esta función permite mostrar los miembros que pertenecen a una institución  
"""
@login_required
def miembros_institucion(request):
	if request.is_ajax():
		args={}
		try:
			institucion = Institucion.objects.get(id_institucion=request.GET['institucion'])
			miembrosActivos= Membresia.objects.filter(fk_institucion=institucion.id_institucion, estado = 1).order_by('fecha_peticion')
			args['miembrosActivos'] = miembrosActivos
			args['numMiembros'] = len(miembrosActivos); 
			args['institucion_nombre'] = request.session['institucion_nombre']
			args['institucion']=institucion
			args.update(csrf(request))
			return render(request,'miembros_institucion.html',args)

		except Institucion.DoesNotExist:
			print 'error no existe institucion'
		except Membresia.DoesNotExist:
			print 'error en miembros'
	else:
		return redirect('/NotFound')


"""
Autor: Rolando Sornoza, Roberto Yoncon
Nombre de funcion: administrar_membresias
Entrada: request POST
Salida: Listado de las memebresias correspondientes la Institucion.
Descripción: Muestra las membresias pendientes y aceptadas y permite modificarlas.
UltimaModificacion: Fausto Mora 1-07-2015
"""

def administrar_membresias(request):
	try:
		institucion_id = request.session['institucion_id']
		institucion = Institucion.objects.get(id_institucion=institucion_id)
		args = {}
		if institucion is not None:
			args['es_admin']=request.session['es_admin']
			args['institucion_nombre'] = request.session['institucion_nombre']
			args['institucion']=institucion
			miembros = Membresia.objects.filter(fk_institucion=institucion.id_institucion)
			args['lista_miembros']=miembros
			args['usuario'] = request.user


		args.update(csrf(request))
		return render_to_response('administrar_membresias.html', args)
	except:
		return redirect('/')




"""
Autor: Leonel Ramirez, Jose Velez
Nombre de funcion: eliminarMensajeRecibido
Entrada: request POST
Salida: elimina mensaje en bandeja de entrada.
Descripción: elimina y actuliza los mensaje del buzon.
"""
@login_required
def eliminarMensajeRecibido(request,):
	sesion=request.session['id_usuario']
	usuario=User.objects.get(id=sesion)
	args = {}
	try:
		idM = int(request.GET.get('q', ''))
		#mensaje =Mensaje.objects.filter(id_mensaje=9)
		#args['mensaje'] = mensaje
		print "MENSAJE: ",idM
		Mensaje.objects.all().filter(id_mensaje=idM).update(visible_receptor=False)
		mensaje=Mensaje.objects.get(id_mensaje = idM)
		mensaje.borrarMensaje()
		#args['mensaje'] = mensaje	
		print "funcion eliminar mensaje:", mensaje.mensaje
	except :
		return HttpResponseRedirect('/BandejaDeEntrada/')


	#print "Eliminar:  ",mensaje
	return HttpResponseRedirect('/BandejaDeEntrada/')

"""
Autor: Leonel Ramirez, Jose Velez
Nombre de funcion: eliminarMensajeEnviado
Entrada: request POST
Salida: elimina mensaje en enviados.
Descripción: elimina y actuliza los mensaje del buzon.
"""
@login_required
def eliminarMensajeEnviado(request,):
	sesion=request.session['id_usuario']
	usuario=User.objects.get(id=sesion)
	args = {}
	try:
		idM = int(request.GET.get('q', ''))
		#mensaje =Mensaje.objects.filter(id_mensaje=9)
		#args['mensaje'] = mensaje
		print "MENSAJE: ",idM
		Mensaje.objects.all().filter(id_mensaje=idM).update(visible_emisor=False)
		mensaje=Mensaje.objects.get(id_mensaje = idM)

		mensaje.borrarMensaje()
		#args['mensaje'] = mensaje	
		print "funcion eliminar mensaje fk_emisor:", mensaje.fk_emisor
		print "funcion eliminar mensaje fk_receptor:", mensaje.fk_receptor
		print "mensaje: ", mensaje.mensaje
	
	except :
		return HttpResponseRedirect('/mensajesEnviados/')


	#print "Eliminar:  ",mensaje
	return HttpResponseRedirect('/mensajesEnviados/')


"""
Autor: Fausto Mora
Nombre de funcion: eliminarMensajeRecibidoInstitucion
Entrada: request POST
Salida: elimina mensaje .
Descripción: marca eliminado mensaje y actuliza template.
"""
@login_required
def eliminarMensajeRecibidoInstitucion(request):
	sesion=request.session['id_usuario']
	usuario=User.objects.get(id=sesion)
	args = {}
	try:
		idM = int(request.GET.get('q', ''))
		#mensaje =Mensaje.objects.filter(id_mensaje=9)
		#args['mensaje'] = mensaje
		print "MENSAJE: ",idM
		Mensaje.objects.all().filter(id_mensaje=idM).update(visible_receptor=False)
		mensaje=Mensaje.objects.get(id_mensaje = idM)

		mensaje.borrarMensaje()
		#args['mensaje'] = mensaje	
		print "funcion eliminar mensaje fk_emisor:", mensaje.fk_emisor
		print "funcion eliminar mensaje fk_receptor:", mensaje.fk_receptor
		print "mensaje: ", mensaje.mensaje
		return HttpResponseRedirect('/BandejaDeEntradaInstitucion/')
	except:
		return HttpResponseRedirect('/BandejaDeEntradaInstitucion/')

"""
Autor: Fausto Mora
Nombre de funcion: eliminarMensajeEnviadoInstitucion
Entrada: request POST
Salida: elimina mensaje en enviados.
Descripción: elimina y actuliza los mensaje del buzon.
"""
@login_required
def eliminarMensajeEnviadoInstitucion(request,):
	sesion=request.session['id_usuario']
	usuario=User.objects.get(id=sesion)
	args = {}
	try:
		idM = int(request.GET.get('q', ''))
		#mensaje =Mensaje.objects.filter(id_mensaje=9)
		#args['mensaje'] = mensaje
		print "MENSAJE: ",idM
		Mensaje.objects.all().filter(id_mensaje=idM).update(visible_emisor=False)
		mensaje=Mensaje.objects.get(id_mensaje = idM)

		mensaje.borrarMensaje()
		#args['mensaje'] = mensaje	
		print "funcion eliminar mensaje fk_emisor:", mensaje.fk_emisor
		print "funcion eliminar mensaje fk_receptor:", mensaje.fk_receptor
		print "mensaje: ", mensaje.mensaje
		return HttpResponseRedirect('/mensajesEnviadosInstitucion/')
	
	except :
		return HttpResponseRedirect('/mensajesEnviadosInstitucion/')

"""
Autor: Fausto Mora
Nombre de funcion: suscribirAInstitucion
Entrada: request POST
Salida: envia una peticion ajax 
Descripción: Esta funcion envia una peticion ajax para 
la suscripcion de un usuario a determinada institucion
"""

def suscribirAInstitucion(request):
	print 'aca dentro suscribirAInstitucion'
	if request.is_ajax():	
		try:
			institucion = Institucion.objects.get(id_institucion=request.POST['institucion'])
			print request.POST['institucion']
			print request.user
			
			solicitudMembresia = Membresia.objects.get(fk_institucion=institucion.id_institucion,fk_usuario=request.user.id)
			print 'imprimiendo membresia'
			print solicitudMembresia.id_membresia

			if solicitudMembresia is not None and solicitudMembresia.estado==-1 :
				solicitudMembresia.cargo = request.POST['cargo']
				solicitudMembresia.descripcion_cargo = request.POST['descripcion']
				solicitudMembresia.fecha_peticion = datetime.datetime.now()
				solicitudMembresia.fecha_aceptacion = None
				solicitudMembresia.estado = 0
				#solicitudMembresia.ip_peticion = socket.gethostbyname(socket.getfqdn())
				solicitudMembresia.ip_peticion = get_client_ip(request)
				solicitudMembresia.save()
				print 'se actualizo parece'
				response = JsonResponse({'save_estado':True})	
				print response
				return HttpResponse(response.content)

		except Institucion.DoesNotExist:
			print 'institucion no existe'
			response = JsonResponse({'save_estado':False})	
			print response
			return HttpResponse(response.content)
		except Membresia.DoesNotExist:
				print 'membresia no existe y se crea una'
				solicitudMembresia = Membresia()
				solicitudMembresia.es_administrator = False
				solicitudMembresia.cargo = request.POST['cargo']
				solicitudMembresia.descripcion_cargo = request.POST['descripcion']
				solicitudMembresia.fecha_peticion = datetime.datetime.now()
				solicitudMembresia.fecha_aceptacion = None
				solicitudMembresia.estado = 0
				#solicitudMembresia.ip_peticion = socket.gethostbyname(socket.getfqdn())
				solicitudMembresia.ip_peticion = get_client_ip(request)
				solicitudMembresia.fk_usuario = request.user
				solicitudMembresia.fk_institucion = institucion
				solicitudMembresia.save()
				print 'se guardo parece'
				response = JsonResponse({'save_estado':True})	
				print response
				return HttpResponse(response.content)
	else:
		print 'no es un ajax - en suscribirAInstitucion'
		return redirect('/')


"""
Autor: Fausto Mora
Nombre de funcion: verificarSuscripcion
Entrada: request get
Salida: envia una peticion ajax 
Descripción: Esta funcion envia una peticion ajax para 
la validar el estado de una suscripcion de un usuario 
"""

def verificarSuscripcion(request):
	if request.is_ajax():
		try:
			institucion = Institucion.objects.get(id_institucion=request.GET['institucion'])
			print institucion.id_institucion
			solicitudMembresia = Membresia.objects.get(fk_institucion=institucion.id_institucion,fk_usuario=request.user.id)
			print solicitudMembresia
			
			if solicitudMembresia is not None:
				existeMembresia = True
				estadoMembresia = solicitudMembresia.estado

			response = JsonResponse({'existeMembresia':existeMembresia,'estadoMembresia':estadoMembresia})	
			return HttpResponse(response.content)
		
		except Membresia.DoesNotExist:
			existeMembresia = False
			estadoMembresia = None

			response = JsonResponse({'existeMembresia':existeMembresia,'estadoMembresia':estadoMembresia})	
			return HttpResponse(response.content)

		except Membresia.MultipleObjectsReturned:
			print 'mas de uno... error, no deberia pasar'
		except Institucion.DoesNotExist:
			print 'institucion no existe' 
	else:
		return redirect('/')

"""
Autor: Fausto Mora
Nombre de funcion: buzonMembresias
Entrada: request get
Salida: envia un HttpResponse
Descripción: Esta funcion carga las membresias en el perfil 
de la institucion
"""

def buzonMembresias(request):
	if request.is_ajax():
		args={}
		try:
			institucion = Institucion.objects.get(id_institucion=request.GET['institucion'])
			membresiasPendientes = Membresia.objects.filter(fk_institucion=institucion.id_institucion, estado = 0).order_by('fecha_peticion')
			args['membresiasPendientes'] = membresiasPendientes
			args['institucion'] = institucion
			args['usuario'] = request.user
			args.update(csrf(request))
			return render(request,'buzon_membresias.html',args)

		except Institucion.DoesNotExist:
			print 'error no existe institucion'
		except Membresia.DoesNotExist:
			print 'error en membresias'
	else:
		return redirect('/')

"""
Autor: Fausto Mora
Nombre de funcion: accionMembresia
Entrada: request post
Salida: envia un response
Descripción: Esta funcion carga maneja la aceptacion y rechazo
de las solicitudes de membresia de una institucion
"""

def accionMembresia(request):
	if request.is_ajax():
		print 'dentro del accionMembresia'
		try:
			membresia = Membresia.objects.get(id_membresia=request.POST['membresia'])
			aux = int(request.POST['accion'])
			if aux == 1:
				membresia.estado = 1
				membresia.fecha_aceptacion = datetime.datetime.now()
			elif aux == 0 :
					membresia.estado = -1

			membresia.save()
			print 'al parecer se guardo'

			try:
				asunto = str(request.POST['asunto']).replace('&#39;','')
				texto_mensaje = request.POST['mensaje']
				print asunto
				print texto_mensaje

				receptor = User.objects.get(username=membresia.fk_usuario.username)
				receptor_aux = Institucion.objects.get(id_institucion=membresia.fk_institucion.id_institucion)
				membresia_institucion = Membresia.objects.get(fk_institucion=receptor_aux,es_administrator=1)
				emisor = User.objects.get(username=membresia_institucion.fk_usuario.username)

				mensajes = Mensaje()
				mensajes.fk_emisor = emisor
				mensajes.fk_receptor = receptor
				mensajes.asunto = asunto
				mensajes.tipo_mensaje = "institucion-usuario"
				mensajes.mensaje= texto_mensaje
				mensajes.fecha_de_envio=datetime.datetime.now()
				mensajes.save()
			except Exception as e:
				print 'error al enviar mensaje'
				print e

			notificacion = Notificacion()
			notificacion.descripcion_notificacion = "Estado de Membresia"
			notificacion.tipo_notificacion = 'accion-membresia'
			notificacion.destinatario_notificacion = membresia.fk_usuario
			notificacion.url_notificacion = 'www.lalal.com'
			notificacion.estado = False
			notificacion.save()
			print 'se guardo notificacion al parecer'

			response = JsonResponse({'membresia_save':True})
			return HttpResponse(response.content)

		except Membresia.DoesNotExist:
			print 'membresia no existe'
			print e
	else:
		return redirect('/')


class AutocompletarUsuario(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self,request,*args,**kwargs):
		user = request.query_params.get('term',None)
		usuarios = User.objects.filter(username__icontains=user)[:5]
		serializador = UsuarioSerializador(usuarios,many=True)
		response = Response(serializador.data)
		return response

def vista_404(request):
	try:
		id_session=request.session['id_user']
	except:
		id_session=None
	args={}
	if id_session is not None:
		tipo404="inicio_view"
	else:
		tipo404="index"
	args['tipo404']=tipo404
	return render_to_response('404.html',args,context_instance=RequestContext(request))
