# -*- encoding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template.context_processors import csrf
from models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

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
		return render_to_response('Usuario_Sign-up.html',{})

