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
	
	return render_to_response('oferta_inicio.html',args)


"""
Autor: Leonel Ramirez
Nombre de funcion: crear_ofertas
Parametros: request
Salida: 
Descripcion: para llamar la pagina oferta inicio
"""
@login_required
def CrearOferta(request):
	args = {}
	return render_to_response('crear_oferta.html',args)


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
Autor: Roberto Yoncon
Nombre de funcion: editar_borrador
Parametros: request
Salida: 
Descripcion: funcion para editar un borrador
"""
@login_required
def editar_borrador(request, id_oferta):
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

	if request.method == 'POST':
		#seccion de informacion
		nombre = request.POST['nombre_oferta']
		tipo = request.POST['select_tipo_oferta']
		descripcion = request.POST['descripcion_oferta']
		dominio = request.POST['oferta_dominio']
		subdominio = request.POST['oferta_sub_dominio']
		#tags = request.POST['oferta_tags'] #Aun no usado
		#seccion de perfiles
		perfilCliente = request.POST['oferta_descripcion_perfil']
		perfilBeneficiario = request.POST['oferta_beneficiario_perfil']
		#seccion de business canvas
		canvasSocioClave = request.POST['canvas_socio_clave']
		canvasActividadesClave = request.POST['canvas_actividades_clave']
		canvasRecursos = request.POST['canvas_recrusos_clave']
		canvasPropuesta = request.POST['canvas_propuesta_valor']
		canvasRelaciones = request.POST['canvas_ralaciones_clientes']
		canvasCanales = request.POST['canvas_canales_distribucion']
		canvasSegmentos = request.POST['canvas_segmentos_clientes']
		canvasEstructura = request.POST['canvas_estructura_costos']
		canvasFuentes = request.POST['canvas_fuente_ingresos']
		#seccion de industria
		tendencias = request.POST['oferta_tendencias']
		solucionesAlternativas = request.POST['ofertas_alternativas_soluciones']
		#para Diagrama de Porter
		porterCompetidores = request.POST['diagramapoter_competidores']
		porterConsumidores = request.POST['diagramapoter_consumidores']
		porterSustitutos = request.POST['diagramapoter_sustitutos']
		porterProveedores = request.POST['diagramapoter_proveedores']
		porterNuevos = request.POST['diagramapoter_nuevos_entrantes']
		#seccion de estado/Logros
		tiempoDisponible = request.POST['oferta_tiempo_disponibilidad']
		tiempoUnidad = request.POST['select_oferta_tiempo']
		propiedadIntelectual = request.POST['oferta_propiedad_intelectual']
		evidenciaTraccion = request.POST['oferta_evidencia_traccion']

		ofertaEditada = oferta
		ofertaEditada.nombre = nombre
		ofertaEditada.tipo = tipo
		ofertaEditada.descripcion = descripcion

		ofertaEditada.dominio = dominio
		ofertaEditada.subdominio = subdominio

		ofertaEditada.perfil_cliente = perfilCliente
		ofertaEditada.perfil_beneficiario = perfilBeneficiario
		ofertaEditada.fk_diagrama_canvas.asociaciones_clave = canvasSocioClave
		ofertaEditada.fk_diagrama_canvas.actividades_clave = canvasActividadesClave
		ofertaEditada.fk_diagrama_canvas.recursos_clave = canvasRecursos
		ofertaEditada.fk_diagrama_canvas.propuesta_valor = canvasPropuesta
		ofertaEditada.fk_diagrama_canvas.relacion_clientes = canvasRelaciones
		ofertaEditada.fk_diagrama_canvas.canales_distribucion = canvasCanales
		ofertaEditada.fk_diagrama_canvas.segmento_mercado = canvasSegmentos
		ofertaEditada.fk_diagrama_canvas.estructura_costos = canvasEstructura
		ofertaEditada.fk_diagrama_canvas.fuente_ingresos = canvasFuentes
		#seccion de industria
		ofertaEditada.cuadro_tendencias_relevantes = tendencias
		ofertaEditada.descripcion_soluciones_existentes = solucionesAlternativas
		#para Diagrama de Porter
		ofertaEditada.fk_diagrama_competidores.competidores = porterCompetidores
		ofertaEditada.fk_diagrama_competidores.consumidores = porterConsumidores
		ofertaEditada.fk_diagrama_competidores.sustitutos = porterSustitutos
		ofertaEditada.fk_diagrama_competidores.proveedores = porterProveedores
		ofertaEditada.fk_diagrama_competidores.nuevosMiembros = porterNuevos
		#seccion de estado/Logros
		#ofertaEditada = tiempoDisponible
		#ofertaEditada = tiempoUnidad
		ofertaEditada.estado_propieada_intelectual = propiedadIntelectual
		ofertaEditada.evidencia_traccion = evidenciaTraccion
		ofertaEditada.save()

		args.update(csrf(request))
		args['es_admin']=request.session['es_admin']
		args['institucion_nombre'] = request.session['institucion_nombre']
		args['oferta'] = ofertaEditada
		return render_to_response('administrar_borrador.html',args)

	else:
		args.update(csrf(request))
		args['es_admin']=request.session['es_admin']
		args['institucion_nombre'] = request.session['institucion_nombre']
		args['oferta'] = oferta
		return render_to_response('editar_borrador.html',args)

