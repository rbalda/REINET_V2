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
from django.contrib.auth.hashers import make_password

def registro_institucion(request):
	return render_to_response('Institucion_Sign-up.html',{})


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
Entrada: request GET
Salida: Formulario de registro usuario
Responde con un formulario vacio de registro de usuario o ejecuta el registro de un usuario
"""
def registro_usuario(request):
	if request.method=='POST':
		#print request.POST
		username=request.POST['username']
		password=request.POST['password1']
		nombres=request.POST['nombres']
		apellidos=request.POST['apellidos']
		cedula=request.POST['cedula']
		cargo=request.POST['cargo']
		telefono=request.POST['telefono']
		actividad=request.POST['actividad']
		website=request.POST['website']
		email=request.POST['email']
		ciudad=request.POST['ciudad']
		fechaNacimiento=request.POST['fechaNacimiento']
		areasInteres=request.POST['areasInteres']
		
		perfil=Perfil()
		perfil.username=username
		perfil.password=make_password(password)
		perfil.first_name=nombres
		perfil.last_name=apellidos
		perfil.cedula=cedula
		perfil.cargo=cargo
		perfil.actividad=actividad
		perfil.web=website
		perfil.email=email
		perfil.ciudad=ciudad
		perfil.fechaNacimiento=fechaNacimiento
		perfil.areasInteres=areasInteres
		perfil.fecharegistro=datetime.datetime.now()
		perfil.reputacion=0
		perfil.estado=1 #estado 1 es activo
		perfil.telefono=telefono
		ubicacion=Ubicacion.objects.get(idubicacion=1)
		perfil.fkubicacion=ubicacion
		perfil.ipregistro=get_client_ip(request)
		print perfil.ipregistro
		perfil.save()
		return HttpResponseRedirect('/index/')	
	else:
		args={}
		args.update(csrf(request))
		return render_to_response('Usuario_Sign-up.html',args)


def index(request):
	return render_to_response('index.html',{})


def signIn(request):

	return render(request,'sign-in.html')


def signUp(request):

	return render(request,'sign-up.html')


def logOut(request):

	logout(request)
	return redirect('/')


def autentificacion(request):
	if request.method=='POST':
		username = request.POST['usernameLogin']
		password = request.POST['passwordLogin']
		print username, password
		usuario = auth.authenticate(username=username,password=password)
		print usuario
		if usuario is not None:
			auth.login(request,usuario)
			request.session['id_usuario']=usuario.id
			return HttpResponseRedirect('/perfilUsuario')
		else:
			error="Nombre de Usuario o Contraseña Incorrectos"
			ctx={'mensajeErrorIngreso':error}
			ctx.update(csrf(request))
			return render_to_response('sign-in.html',ctx)
	else:
		print "Error en el request.POST"



@login_required
def perfilUsuario(request):

	session = request.session['id_usuario']
	usuario = User.objects.get(id=session)
	args={}


	if usuario is not None:
		args['usuario']=usuario

	else:
		args['error']="Error al cargar los datos"


	args.update(csrf(request))
	return render_to_response('profile_usuario.html',args)
