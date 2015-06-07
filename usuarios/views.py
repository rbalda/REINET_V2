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
from .models import *
from django.contrib.auth.forms import UserCreationForm


def registro_institucion(request):
	return render_to_response('Institucion_Sign-up.html',{})

"""
Autor: Angel Guale
Nombre de funcion: registro_usuario 
Entrada: request GET
Salida: Formulario de registro usuario
Responde con un formulario vacio de registro de usuario
"""
def registro_usuario(request):
	if request.method=='POST':
		print request.POST
		username=request.POST['username']
		nombres=request.POST['nombres']
		apellidos=request.POST['apellidos']
		cedula=request.POST['cedula']
		cargo=request.POST['cargo']
		actividad=request.POST['actividad']
		website=request.POST['website']
		email=request.POST['email']
		ciudad=request.POST['ciudad']
		fechaNacimiento=request.POST['fechaNacimiento']
		areasInteres=request.POST['areasInteres']
		pass	
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
		usuario = auth.authenticate(username=username,password=password)

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
