# -*- encoding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template.context_processors import csrf
from models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import datetime

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
		perfil.password=password
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
