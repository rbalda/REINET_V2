# Create your views here.
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

from ofertas_demandas.models import *
from ofertas_demandas.serializers import *

from usuarios.models import *

"""
Autor: Leonel Ramirez
Nombre de funcion: InicioOferta
Parametros: request
Salida: 
Descripcion: para llamar la pagina oferta inicio
"""

@login_required
def InicioOferta(request):
	args = {}
	args['usuario']=request.user
	return render_to_response('oferta_inicio.html',args)


"""
Autor: FaustoMora
Nombre de funcion: crear_ofertas
Parametros: request
Salida: 
Descripcion: para llamar la pagina oferta inicio
"""
@login_required
def CrearOfertaCopia(request):
	if request.GET.get('select_oferta',False):
		args = {}
		args['usuario']=request.user
		oferta = None
		oferta_id = request.GET['select_oferta']
		oferta = Oferta.objects.get(id_oferta=oferta_id)
		args['oferta']=oferta
		args.update(csrf(request))
		return render(request,'crear_oferta.html',args)
	else:
		return redirect('/CrearOferta/')

@login_required
def CrearOferta(request):
	args = {}
	args['usuario']=request.user
	args.update(csrf(request))
	return render(request,'crear_oferta.html',args)


"""
Autor: Roberto Yoncon
Nombre de funcion: verCualquierOferta
Parametros: request
Salida: http
Descripcion: funcion para ver una oferta publicada
"""
@login_required
def verCualquierOferta(request, id_oferta):
	session = request.session['id_usuario']
	usuario = Perfil.objects.get(id=session)
	args = {}

	if usuario is not None:
		#Guardo en la variable de sesion a usuario.
		args['usuario'] = usuario

	else:
		args['error'] = "Error al cargar los datos"
		return HttpResponseRedirect('/NotFound/')

	try:
		oferta = Oferta.objects.get(id_oferta = id_oferta)
	except:
		return HttpResponseRedirect('/NotFound/')

	membresiaOferta = MiembroEquipo.objects.all().filter(fk_participante = usuario.id_perfil, fk_oferta_en_que_participa = id_oferta, es_propietario = 1).first()

	if membresiaOferta is not None:
		return HttpResponseRedirect('/NotFound/')

	args.update(csrf(request))
	args['es_admin']=request.session['es_admin']
	args['institucion_nombre'] = request.session['institucion_nombre']
	args['oferta'] = oferta
	return render_to_response('oferta_ver_otra.html',args)

"""
Autor: Pedro Iniguez
Nombre de funcion: administrarOferta
Parametros: request
Salida: 
Descripcion: funcion para administrar mi oferta publicada.
"""

@login_required
def administrar_Oferta(request, id_oferta):
	session = request.session['id_usuario']
	usuario = Perfil.objects.get(id=session)
	args = {}

	if usuario is not None:
		#Guardo en la variable de sesion a usuario.
		args['usuario'] = usuario

	else:
		args['error'] = "Error al cargar los datos"
		return HttpResponseRedirect('/NotFound/')

	try:
		oferta = Oferta.objects.get(id_oferta = id_oferta)
	except:
		return HttpResponseRedirect('/NotFound/')
	if (oferta.publicada == 0):
		return HttpResponseRedirect('/NotFound/')
	membresiaOferta = MiembroEquipo.objects.all().filter(fk_participante = usuario.id_perfil, fk_oferta_en_que_participa = id_oferta, es_propietario = 1).first()

	if membresiaOferta is None:
		return HttpResponseRedirect('/NotFound/')
	args.update(csrf(request))
	args['es_admin']=request.session['es_admin']
	args['institucion_nombre'] = request.session['institucion_nombre']
	args['oferta'] = oferta
	return render_to_response('administrar_oferta.html',args)

"""
Autor: Pedro Iniguez
Nombre de funcion: administarBorrador
Parametros: request
Salida: 
Descripcion: funcion para administrar mi oferta publicada.
"""

@login_required
def administrar_Borrador(request, id_oferta):
	session = request.session['id_usuario']
	usuario = Perfil.objects.get(id=session)
	args = {}

	if usuario is not None:
		#Guardo en la variable de sesion a usuario.
		args['usuario'] = usuario

	else:
		args['error'] = "Error al cargar los datos"
		return HttpResponseRedirect('/NotFound/')

	try:
		oferta = Oferta.objects.get(id_oferta = id_oferta)
	except:
		return HttpResponseRedirect('/NotFound/')
	if (oferta.publicada == 1):
		return HttpResponseRedirect('/NotFound/')
	membresiaOferta = MiembroEquipo.objects.all().filter(fk_participante = usuario.id_perfil, fk_oferta_en_que_participa = id_oferta, es_propietario = 1).first()

	if membresiaOferta is None:
		return HttpResponseRedirect('/NotFound/')

	args.update(csrf(request))
	args['es_admin']=request.session['es_admin']
	args['institucion_nombre'] = request.session['institucion_nombre']
	args['oferta'] = oferta
	return render_to_response('administrar_borrador.html',args)

"""
Autor: Jose Velez Gomez
Nombre de funcion: editar_borrador
Parametros: request
Salida: 
Descripcion: funcion para editar un borrador
"""
@login_required
def editar_borrador(request):
	args = {}
	return render_to_response('editar_borrador.html',args)

