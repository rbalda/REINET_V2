# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import datetime
from .models import *

from django.contrib.auth.forms import UserCreationForm

"""
Autor: Pedro Aim
Nombre de funcion: registro_institucion
Entrada: request GET o POST
Salida: pagina para el Ingreso de codigo si es GET, debe devolver perfil de la institucion creada
Corresponde a la creacion de la institucion y el anexo con e usuario por medio de membresia, asi como update a la tabla peticion con valor 1 pues se usa el codigo
"""
@login_required
def registro_institucion(request):
	if request.method == 'GET':
		session = request.session['id_usuario']
		usuario = Perfil.objects.get(id=session)
		args={}

		if usuario is not None:
			args['usuario']=usuario

		else:
			args['error']="Error al cargar los datos"

		args.update(csrf(request))
		return render_to_response('Institucion_Sign-up.html', args)
	else:
		print "es post"
		try:
			peticion = Peticion.objects.all().filter(fk_usuario = request.session['id_usuario']).first()
			if (peticion.usado == 0) :
				print "peticion no usada"
				siglas=request.POST['siglaInstitucion']
				desc=request.POST['descInstitucion']
				mision=request.POST['misionInstitucion']
				ub=request.POST['ubicacionInstitucion']
				recursos=request.POST['recursosInstitucion']
				web=request.POST['webInstitucion']
				mail=request.POST['emailInstitucion']
				telf=request.POST['telefonoInstitucion']
				cargo = request.POST['cargoInstitucion']
				cargo_desc = request.POST['cargoDescInstitucion']
				try:
					image = request.FILES['logo']
				except:
					image = "noPicture.png"
				insti = Institucion();
				insti.nombre = peticion.nombre_institucion
				insti.siglas = siglas
				insti.logo = image
				insti.descripcion = desc
				insti.mision = mision
				insti.ubicacion = ub
				insti.web = web
				insti.recursos_ofrecidos = recursos
				insti.correo = mail
				insti.telefono_contacto = telf
				ciudad=City.objects.get(id=1)
				pais=Country.objects.get(id=1)
				insti.ciudad = ciudad
				insti.pais = pais
				insti.save()

				peticion.usado = 1
				peticion.save()

				membresia = Membresia()
				membresia.es_administrator = 1
				membresia.cargo = cargo
				membresia.descripcion_cargo = cargo_desc
				membresia.fecha_peticion = '2015-06-10'
				membresia.fecha_aceptacion = '2015-06-10'
				membresia.ip_peticion = '127.0.0.1'
				membresia.estado = 1
				membresia.fk_institucion = insti
				membresia.fk_usuario = Perfil.objects.get(id = request.session['id_usuario'])
				membresia.save()
				print "registros guardados"
				try:
					membresiaBorrar=Membresia.objects.filter(fk_usuario = request.session['id_usuario'], fk_institucion = 1).first()
					membresiaBorrar.delete()
					print "membresia independiente deleted"
				except:
					print "membresia no encontrada"
				return redirect('/inicioUsuario')
			else:
				print "peticion ya usada"
				return redirect('/registro_institucion')
		except:
			print "algo fallo"
			return redirect('/registro_institucion')

"""
Autor: Angel Guale
Nombre de funcion: get_client_ip 
Entrada: request 
Salida: obtiene ip del cliente
"""

def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip
"""
Autor: Angel Guale
Nombre de funcion: registro_usuario 
Entrada: request GET o POST
Salida: Formulario de registro usuario
Responde con un formulario vacio de registro de usuario o ejecuta el registro de un usuario
"""
def registro_usuario(request):
	if request.method=='POST':
		#print request.POST
        #formulario = Form(request.POST)
		username=request.POST['username']
		password=request.POST['password1']
		nombres=request.POST['nombres']
		apellidos=request.POST['apellidos']
		cedula=request.POST['cedula']
		#cargo=request.POST['cargo']
		telefono=request.POST['telefono']
		#actividad=request.POST['actividad']
		website=request.POST['website']
		email=request.POST['email']
		pais_selected=request.POST['pais']
		print pais_selected

		perfil=Perfil()
		perfil.username=username
		perfil.set_password(password)
		perfil.first_name=nombres
		perfil.last_name=apellidos
		perfil.cedula=cedula
		#perfil.cargo=cargo
		#perfil.actividad=actividad
		perfil.web=website
		perfil.email=email
		#perfil.ciudad=ciudad
		#perfil.fechaNacimiento=fechaNacimiento
		#perfil.areasInteres=areasInteres
		perfil.fecha_registro=datetime.datetime.now()
		perfil.reputacion=0
		perfil.estado=1 #estado 1 es activo
		perfil.telefono=telefono
		#ubicacion=Ubicacion.objects.get(idubicacion=1)
		pais=Country.objects.get(id=pais_selected)
		ciudad=City.objects.get(id=1)
		#pais=Country.objects.get(id=1)
		perfil.fk_ciudad=ciudad
		perfil.fk_pais=pais
		perfil.ip_registro=get_client_ip(request)
		perfil.save()

		membresia=Membresia()
		membresia.es_administrator=0 #0 para falso
		membresia.cargo=""
		membresia.descripcion=""
		membresia.fecha_aceptacion=datetime.datetime.now()
		membresia.fecha_peticion=datetime.datetime.now()
		membresia.ip_peticion=get_client_ip(request)
		membresia.estado=1 #1 es para aceptado
		institucion=Institucion.objects.get(siglas="I")
		membresia.fk_institucion=institucion
		membresia.fk_usuario=perfil
		membresia.save()

		return HttpResponseRedirect('/signIn/')
	else:
		args={}
		args.update(csrf(request))
		paises=Country.objects.all()
		args['paises']=paises
		return render_to_response('Usuario_Sign-up.html',args)


def index(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('/inicioUsuario')
	else:
		return render_to_response('index.html',{})


def signIn(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/inicioUsuario/')
	else:
		return render(request,'sign-in.html')


def signUp(request):

	return render(request,'sign-up.html')


def logOut(request):

	logout(request)
	return redirect('/')

@login_required
def editar_usuario(request):
	session = request.session['id_usuario']
	usuario = Perfil.objects.get(id=session)
	args={}

	if usuario is not None:
		args['usuario']=usuario
	else:
		args['error']="Error al cargar los datos"


	if request.method=='POST':
		#print request.POST
		nombres=request.POST['nombres']
		apellidos=request.POST['apellidos']
		cedula=request.POST['cedula']
		#cargo=request.POST['cargo']
		telefono=request.POST['telefono']
		#actividad=request.POST['actividad']
		website=request.POST['website']
		email=request.POST['email']

		perfil=usuario
		perfil.first_name=nombres
		perfil.last_name=apellidos
		perfil.cedula=cedula
		#perfil.cargo=cargo
		#perfil.actividad=actividad
		perfil.web=website
		perfil.email=email
		#perfil.ciudad=ciudad
		#perfil.fechaNacimiento=fechaNacimiento
		#perfil.areasInteres=areasInteres
		perfil.fecharegistro=datetime.datetime.now()
		perfil.telefono=telefono
		#ubicacion=Ubicacion.objects.get(idubicacion=1)
		#perfil.fkubicacion=ubicacion
		perfil.save()

		return HttpResponseRedirect('/perfilUsuario/')
	else:
		args.update(csrf(request))
		return render_to_response('Usuario_Edit-Profile.html',args)


def autentificacion(request):
	if request.method=='POST':
		username = request.POST['usernameLogin']
		password = request.POST['passwordLogin']
		usuario = auth.authenticate(username=username,password=password)
		args={}
		
		if usuario is not None:
			auth.login(request,usuario)
			request.session['id_usuario']=usuario.id
			return HttpResponseRedirect('/inicioUsuario')
		else:
			error="Nombre de Usuario o Contraseña Incorrectos"
			args['mensajeErrorIngreso']=error
			args.update(csrf(request))
			return render_to_response('sign-in.html',ctx)
	else:
		print "Error en el request.POST"


def terms(request):

	return render(request, 'terms.html')

@login_required
def inicio(request):

	session = request.session['id_usuario']
	usuario = Perfil.objects.get(id=session)
	args={}

	if usuario is not None:
		args['usuario']=usuario

	else:
		args['error']="Error al cargar los datos"


	args.update(csrf(request))
	return render_to_response('Usuario_Home.html',args)


@login_required
def perfilUsuario(request):
	session = request.session['id_usuario']
	usuario = Perfil.objects.get(id=session)
	args={}

	if usuario is not None:
		args['usuario']=usuario
		usuario.estado = 1
		usuario.save()

		membresia=Membresia.objects.filter(fk_usuario=usuario.id)
		#print membresia[0].idmembresia
		institucion=Institucion.objects.get(id_institucion=membresia[0].fk_institucion.id_institucion)
		#print institucion
		args['institucion']=institucion

	else:
		args['error']="Error al cargar los datos"
		return HttpResponseRedirect('/signIn/')


	args.update(csrf(request))
	#args['usuario']=usuario
	return render_to_response('profile_usuario.html',args)


"""
Autor: Edinson Sánchez
Nombre de funcion: perfilInstitucion
Entrada: request GET
Salida: Perfil de Institucion
"""
@login_required
def perfilInstitucion(request):
	session = request.session['id_usuario']
	usuario = Perfil.objects.get(id=session)
	args={}

	if usuario is not None:
		args['usuario']=usuario
		membresia=Membresia.objects.filter(fkusuario=usuario.id,esadministrator=1).first()
		print "sadhas"
		if membresia.esadministrator == 1:
			print "entre"
			print membresia.idmembresia
			institucion=Institucion.objects.get(idinstitucion=membresia.fkinstitucion.idinstitucion)
			#print institucion
			args['institucion']=institucion
		else:
			print "aca"
			args['error1']="Usted no es miembro de ninguna Institucion"

	else:
		args['error']="Error al cargar los datos"
		return HttpResponseRedirect('/signIn/')


	args.update(csrf(request))
	#args['usuario']=usuario
	return render_to_response('profile_institucion.html',args)


"""
Autor: Pedro Aim
Nombre de funcion: verCodigo
Entrada: request POST
Salida: Formulario de registro institucion
Responde con un formulario vacio de registro de institucion
"""
@login_required
def verCodigo(request):
	if request.method == 'POST':
		args={}
		codigo = request.POST['codigo']
		print codigo
		peticion = Peticion.objects.all().filter(fk_usuario = request.session['id_usuario']).first()
		try :
			print peticion.codigo
			if (peticion.codigo == codigo and peticion.usado == 0) :
				args['codigo'] = peticion.codigo
				args['insti'] = peticion.nombre_institucion
				return render_to_response('institucion_form_response.html', args)
			else :
				return render_to_response('codigo_usado.html')
		except:
			return render_to_response('nocodigo.html')


@login_required
def suspenderUsuario(request):

	usuario = Perfil.objects.get(id=request.session['id_usuario'])
	password_ingresada = request.POST['txt_password_ingresada']

	if usuario.check_password(password_ingresada):
		#Cero significa que esta inactivo
		usuario.estado = 0
		usuario.save()
		return logOut(request)
	else:
		args={}
		error = "Contraseña Incorrecta"
		args['error']= error
		args['usuario']=usuario
		args.update(csrf(request))
		return render(request,'Usuario_Edit-Profile.html',args)

"""
Autor: Angel Guale
Nombre de funcion: generarCodigo 
Entrada: request GET o POST
Salida: Formulario de generarCodigo 
Genera un codigo para registrar institucion
"""

def generarCodigo(request):
	if request.method=='POST':
		username=request.POST['username']
		usuario = Perfil.objects.get(username=username)
		codigo=request.POST['codigo']
		nombre_institucion=request.POST['nombre_institucion']
		#creo el registro de peticion
		peticion=Peticion()
		peticion.codigo=codigo
		peticion.nombre_institucion=nombre_institucion
		peticion.usado=0
		peticion.fk_usuario=usuario
		peticion.save()
		args={}
		args['mensaje']="Codigo Institucion generado"
		return render_to_response('Administrador_generar_codigo.html', args)
	else:
		args={}
		args.update(csrf(request))

		return render_to_response('Administrador_generar_codigo.html', args)



