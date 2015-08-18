# -*- encoding: utf-8 -*-
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
from usuarios.serializers import UsuarioSerializador

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
		palabra_clave = PalabraClave.objects.filter(ofertas_con_esta_palabra=oferta)
		tags = []
		for t in palabra_clave:
			tags.append(t.palabra)

		args['oferta']=oferta
		args['tags']=tags
		args.update(csrf(request))
		return render(request,'crear_oferta.html',args)
	else:
		return redirect('/CrearOferta/')

@login_required
def CrearOferta(request):
	args = {}
	args['usuario']=request.user
	args['oferta'] = None
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
		try:
			oferta = Oferta.objects.get(id_oferta = id_oferta)
			args['oferta'] = oferta
		except:
			args['mensaje_error'] = "La oferta no se encuentra en la red, lo sentimos."
			return render_to_response('problema_oferta.html',args)

		try:
			membresiaOferta = MiembroEquipo.objects.get(fk_participante = usuario.id_perfil, fk_oferta_en_que_participa = oferta.id_oferta)
			estadoMembresia = membresiaOferta.estado_membresia
			args['estadoMembresia'] = estadoMembresia
		except Exception as e:
			args['estadoMembresia'] = 2


		if oferta.publicada == 0 :
			args.update(csrf(request))
			args['es_admin']=request.session['es_admin']
			args['mensaje_error'] = "La oferta "+oferta.nombre+", no esta actualmente publicada."
			return render_to_response('problema_oferta.html',args)

		else:
			participantes = MiembroEquipo.objects.filter(fk_oferta_en_que_participa=id_oferta,estado_membresia=1)
			propietario = MiembroEquipo.objects.get(fk_oferta_en_que_participa=id_oferta,estado_membresia=1,es_propietario=1).fk_participante
			comentariosOferta = ComentarioCalificacion.objects.filter(fk_oferta_id=id_oferta)
			calificacionOferta = oferta.calificacion_total

		args.update(csrf(request))
		args['es_admin']=request.session['es_admin']
		args['participantes'] = participantes
		args['comentariosOferta'] = comentariosOferta
		args['calificacionOferta'] = range(int(calificacionOferta))
		args['propietario'] = propietario
		return render_to_response('oferta_ver_otra.html',args)

	else:
		args['error'] = "Error al cargar los datos"
		return HttpResponseRedirect('/NotFound/')


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
	print 'mi id antes'+id_oferta
	if usuario is not None:
		#Guardo en la variable de sesion a usuario.
		args['usuario'] = usuario
	else:
		args['error'] = "Error al cargar los datos"
		return HttpResponseRedirect('/NotFound/')

	oferta = Oferta.objects.get(id_oferta = id_oferta)
	print oferta.id_oferta


	if (oferta.publicada == 0):
		print 'No publicada'
		#return HttpResponseRedirect('/NotFound/')
	membresiaOferta = MiembroEquipo.objects.all().filter(fk_participante = usuario.id_perfil, fk_oferta_en_que_participa = id_oferta, es_propietario = 1).first()

	if membresiaOferta is None:
		return HttpResponseRedirect('/NotFound/')


	solicitudes=MiembroEquipo.objects.all().filter(fk_oferta_en_que_participa = id_oferta, estado_membresia=0)

	participantes = MiembroEquipo.objects.all().filter(fk_oferta_en_que_participa=oferta.id_oferta,estado_membresia=1)

	equipoDueno = MiembroEquipo.objects.all().filter(es_propietario=1, fk_oferta_en_que_participa=oferta.id_oferta).first()

	args.update(csrf(request))
	args['dueno'] = equipoDueno.fk_participante.first_name + ' ' + equipoDueno.fk_participante.last_name
	args['es_admin']=request.session['es_admin']
	args['institucion_nombre'] = request.session['institucion_nombre']
	args['oferta'] = oferta
	args['participantes'] = participantes
	args['solicitudes']=solicitudes
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

	equipoDueno = MiembroEquipo.objects.all().filter(es_propietario=1, fk_oferta_en_que_participa=oferta.id_oferta).first()

	args.update(csrf(request))
	args['dueno'] = equipoDueno.fk_participante.first_name + ' ' + equipoDueno.fk_participante.last_name
	args['es_admin']=request.session['es_admin']
	args['institucion_nombre'] = request.session['institucion_nombre']
	args['oferta'] = oferta
	return render_to_response('administrar_borrador.html',args)

"""
Autor: Roberto Yoncon
Nombre de funcion: editar_borrador
Parametros: request, id de una oferta
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



"""
Autor: David Vinces
Nombre de la funcion: listaComentariosAceptados
Entrada:
Salida: Muestra la lista de Comentarios Aceptados de una oferta
Descripción:Esta función permite mostrar el listado de comentarios aceptados de una oferta
"""
@login_required
def listaComentariosAceptados(request):
	print 'listaComentariosAceptados :: ajax con id '+ request.GET['oferta']
	if request.is_ajax():
		args={}
		try:
			oferta = Oferta.objects.get(id_oferta=request.GET['oferta'])
			listaComentarios= ComentarioCalificacion.objects.filter(fk_oferta = oferta.id_oferta)
			args['listaComentarios'] = listaComentarios
			args['oferta']=oferta
			args.update(csrf(request))
			return render(request,'comentario_oferta.html',args)
		except Oferta.DoesNotExist:
			print '>> Oferta no existe'
		except ComentarioCalificacion.DoesNotExist:
			print '>> Comentario no existe'
		except:
			print '>> Excepcion no controlada'
	else:
		return redirect('/NotFound')


"""
Autor: Ray Montiel
Nombre de la funcion: equipoOferta
Entrada:
Salida: Muestra el equipo de una oferta
Descripción:Esta función permite mostrar el equipo de una oferta
"""
@login_required
def equipoOferta(request):
	print 'entrare al ajax con id '+ request.GET['oferta']
	if request.is_ajax():
		print 'estoy en el ajax'
		args={}
		try:
			oferta = Oferta.objects.get(id_oferta=request.GET['oferta'])
			listaEquipo= MiembroEquipo.objects.filter(fk_oferta_en_que_participa = oferta.id_oferta)
			args['listaEquipo'] = listaEquipo
			args['oferta']=oferta
			args.update(csrf(request))
			return render(request,'equipo_oferta.html',args)

		except Oferta.DoesNotExist:
			print 'esa oferta no existe '
			return redirect('/')
		except MiembroEquipo.DoesNotExist:
			print 'Este pana no tiene amigos :/'
			return redirect('/')
		except:
			print 'ya me jodi =('
			return redirect('/')
	else:
		return redirect('/NotFound')

@login_required
def equipoEditableOferta(request):

	if request.is_ajax():

		args={}
		try:
			oferta = Oferta.objects.get(id_oferta=request.GET['oferta'])
			listaEquipo= MiembroEquipo.objects.filter(fk_oferta_en_que_participa = oferta.id_oferta, estado_membresia=1)
			args['listaEquipo'] = listaEquipo
			args['oferta']=oferta
			args.update(csrf(request))
			return render(request,'equipo_editable.html',args)

		except Oferta.DoesNotExist:
			print 'esa oferta no existe '
			return redirect('/')
		except MiembroEquipo.DoesNotExist:
			print 'Este pana no tiene amigos :/'
			return redirect('/')
		except:
			print 'ya me jodi =('
			return redirect('/')
	else:
		return redirect('/NotFound')



"""
Autor: Ray Montiel
Nombre de la funcion: AutocompletarParticipante
Entrada:
Salida: Muestra los usuarios disponibles para agregarlos a la oferta
Descripción:Esta función permite mostrar los participantes autocompletando sus nombres y usernames
"""
class AutocompletarParticipante(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self,request,*args,**kwargs):
		user = request.query_params.get('term',None)
		usuarios = User.objects.filter(username__icontains=user)[:5]
		serializador = UsuarioSerializador(usuarios,many=True)
		response = Response(serializador.data)
		return response


"""
Autor: Ray Montiel
Nombre de la funcion: editarEquipoOferta
Entrada:
Salida: Muestra el equipo de una oferta para poderlo editar desde Administrar oferta
Descripción:Esta función permite mostrar el equipo de una oferta para poderlo editar desde Administrar oferta

@login_required
def editarEquipoOferta(request):
	if request.is_ajax():
		args={}
		try:
			ofertaEditar = Oferta.objects.get(id_oferta=request.GET['oferta'])
			listaEditarEquipo= MiembroEquipo.objects.filter(fk_oferta_en_que_participa = ofertaEditar.id_oferta,estado_membresia=1)
			args['listaEditarEquipo'] = listaEditarEquipo
			args['oferta']=ofertaEditar
			args.update(csrf(request))
			return render(request,'equipo_editar_oferta.html',args)
		except Oferta.DoesNotExist:
			print 'esa oferta no existe '
			return redirect('/')
		except MiembroEquipo.DoesNotExist:
			print 'Este pana no tiene amigos :/'
			return redirect('/')
		except:
			print 'ya me jodi =('
			return redirect('/')
	else:
		return redirect('/NotFound')
"""
"""
Autor: Ray Montiel
Nombre de la funcion: solicitarMembresiaOferta
Entrada:
Salida:
Descripción:Envia una solicitud para participar en una Oferta
"""
@login_required
def solicitarMembresiaOferta(request):
	if request.method=="POST":
		try:
			oferta = Oferta.objects.get(id_oferta=request.POST['oferta'])
			print request.POST['oferta']
			print request.user

			solicitudMembresia = MiembroEquipo.objects.get(fk_oferta_en_que_participa=oferta.id_oferta,fk_participante=request.user.id)

			if solicitudMembresia is not None and solicitudMembresia.estado==-1 :
				solicitudMembresia.rol_participante = "Miembro del Equipo de la Oferta"
				solicitudMembresia.estado_membresia = 0
				solicitudMembresia.fecha_aceptacion = datetime.datetime.now()
				solicitudMembresia.comentario_peticion= request.POST['comentario_peticion']
				solicitudMembresia.save()
				print 'se actualizo parece'
				response = JsonResponse({'save_estado':True})
				return HttpResponse(response.content)

		except Oferta.DoesNotExist:
			print 'Oferta no existe'
			return redirect('/')
		except MiembroEquipo.DoesNotExist:
				solicitudMembresia = MiembroEquipo()
				solicitudMembresia.es_propietario = False
				solicitudMembresia.rol_participante = "Miembro del Equipo de la Oferta"
				solicitudMembresia.estado_membresia = 0
				solicitudMembresia.fk_participante = request.user.perfil
				solicitudMembresia.fk_oferta_en_que_participa = oferta
				solicitudMembresia.fecha_aceptacion = datetime.datetime.now()
				solicitudMembresia.comentario_peticion= request.POST['comentario_peticion']
				solicitudMembresia.save()
				print 'se guardo parece'
				response = JsonResponse({'save_estado':True})
				return HttpResponse(response.content)
		except:
			print "error"
			return "error"
	else:
		return redirect('/')

"""
Autor: Ray Montiel
Nombre de la funcion: agregarParticipante
Entrada: nombre de usuario y rol
Salida:
Descripción:Agrega a un participante a una oferta
"""
def agregarParticipante(request):
	if request.method=="POST":
		session = request.session['id_usuario']
		usuario = Perfil.objects.get(id=session)
		args = {}

		participante = Perfil.objects.get(username = request.POST['particOferta'])
		print participante.username
		rol = request.POST['rolNuevoIntegrante']
		print rol
		ofertaAdmin = request.POST['ofertaAdmin']
		if usuario is not None:
			#Guardo en la variable de sesion a usuario.
			args['usuario'] = usuario
			print usuario.username
		else:
			args['error'] = "Error al cargar los datos"
			return HttpResponseRedirect('/NotFound/')

		try:
			oferta = Oferta.objects.get(id_oferta=ofertaAdmin)
			membresia = MiembroEquipo.objects.get(fk_oferta_en_que_participa=oferta.id_oferta,fk_participante = participante)

			if membresia is not None:
				print 'ya es miembro ese bronza'
				return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

		except Oferta.DoesNotExist:
			print 'Oferta no existe'
			oferta = None
		except MiembroEquipo.DoesNotExist:
			print 'Membresia no existe'
			membresia = MiembroEquipo()
			membresia.es_propietario = False
			membresia.rol_participante = rol
			membresia.estado_membresia = 1
			membresia.fk_participante = participante.perfil
			membresia.fk_oferta_en_que_participa = oferta
			membresia.fecha_aceptacion = datetime.datetime.now()
			membresia.save()

	else:
		return HttpResponseRedirect('/Not Found')











"""
Autor: Ray Montiel
Nombre de la funcion: verificaParticipacion
Entrada:
Salida:Habilita o inhabilita el boton de membresia
Descripción:Verifica que la solicitud para participar en una Oferta sea valida


def verificaParticipacion(request):
	if request.is_ajax():
		try:
			oferta = Oferta.objects.get(id_oferta=request.GET['oferta'])
			print oferta.id_oferta
			solicitudMembresia = MiembroEquipo.objects.get(fk_oferta_en_que_participa=oferta.id_oferta,fk_participante=request.user.id)
			print solicitudMembresia + 'lol que bronza'

			if solicitudMembresia is not None:
				print 'si existe membresia'
				participantes = oferta.equipo.count
				existeMembresia = True
				estadoMembresia = solicitudMembresia.estado_membresia

			response = JsonResponse({'existeMembresia':existeMembresia,'estadoMembresia':estadoMembresia,'participantes':participantes})
			return HttpResponse(response.content)

		except MiembroEquipo.DoesNotExist:
			print 'no existe membresia'
			participantes = oferta.equipo.count
			existeMembresia = False
			estadoMembresia = None

			response = JsonResponse({'existeMembresia':existeMembresia,'estadoMembresia':estadoMembresia,'participantes':participantes})
			return HttpResponse(response.content)

		except MiembroEquipo.MultipleObjectsReturned:
			print 'mas de uno... error, no deberia pasar'
		except Oferta.DoesNotExist:
			print 'Oferta no existe'
	else:
		return redirect('/')
"""

"""
Autor: Roberto Yoncon
Nombre de funcion: publicar_borrador
Parametros: request, id de una oferta
Salida: 
Descripcion: cambia el estado de una oferta de 
"""
@login_required
def publicar_borrador(request, id_oferta):
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

	oferta.publicada = 1
	oferta.save()

	args['es_admin']=request.session['es_admin']
	args['oferta'] = oferta
	return render_to_response('oferta_inicio.html',args)



"""
Autor: Roberto Yoncon
Nombre de funcion: publicar_borrador
Parametros: request, id de una oferta
Salida: 
Descripcion: cambia el estado de una oferta de 
"""
@login_required
def eliminar_borrador(request, id_oferta):
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

	oferta.delete()
	
	args['es_admin']=request.session['es_admin']
	return render_to_response('oferta_inicio.html',args)



"""Autor: Angel Guale

"""
def aceptar_peticion(request):
	if request.method=="POST":
		session = request.session['id_usuario']
		usuario = Perfil.objects.get(id=session)
		id_user_peticion=request.POST["id_user_peticion"]
		id_oferta=request.POST["id_oferta"]
		rol_participante=request.POST["rol"]
		args = {}
		oferta=Oferta.objects.get(id_oferta=id_oferta);
		solicitudMembresia = MiembroEquipo.objects.filter(fk_oferta_en_que_participa=id_oferta,fk_participante=id_user_peticion).first()
		if solicitudMembresia is not None:
			solicitudMembresia.estado_membresia=1
			solicitudMembresia.rol_participante=rol_participante
			solicitudMembresia.save()
			#response = JsonResponse({'aceptado':"True"})
			#return HttpResponse(response.content)
			return HttpResponse("ok")
		else:
			print "No existe una peticion"
			#response = JsonResponse({'aceptado':"False"})
			#return HttpResponse(response.content)
			return HttpResponse("No existe una peticion")
	else:
		return HttpResponseRedirect('NotFound');

def editar_rol_membresia(request):
	if request.method=="POST":
		session = request.session['id_usuario']
		usuario = Perfil.objects.get(id=session)
		id_user_peticion=request.POST["id_user_editable"]
		id_oferta=request.POST["id_oferta"]
		rol_participante=request.POST["rol"]
		args = {}
		oferta=Oferta.objects.get(id_oferta=id_oferta);
		solicitudMembresia = MiembroEquipo.objects.filter(fk_oferta_en_que_participa=id_oferta,fk_participante=id_user_peticion).first()
		if solicitudMembresia is not None:
			solicitudMembresia.rol_participante=rol_participante
			solicitudMembresia.save()
			#response = JsonResponse({'aceptado':"True"})
			#return HttpResponse(response.content)
			return HttpResponse("ok")
		else:
			print "No existe una peticion"
			#response = JsonResponse({'aceptado':"False"})
			#return HttpResponse(response.content)
			return HttpResponse("No existe una peticion")
	else:
		return HttpResponseRedirect('NotFound');

def editar_estado_membresia(request):
	if request.method=="POST":
		session = request.session['id_usuario']
		usuario = Perfil.objects.get(id=session)
		id_user_peticion=request.POST["id_user_editable"]
		id_oferta=request.POST["id_oferta"]
		estado_str=request.POST["estado"]
		activo=1
		if estado_str=="ACTIVO":
			activo=1
		else:
			activo=0

		args = {}
		oferta=Oferta.objects.get(id_oferta=id_oferta);
		solicitudMembresia = MiembroEquipo.objects.filter(fk_oferta_en_que_participa=id_oferta,fk_participante=id_user_peticion).first()
		if solicitudMembresia is not None:
			solicitudMembresia.activo=activo
			solicitudMembresia.save()
			#response = JsonResponse({'aceptado':"True"})
			#return HttpResponse(response.content)
			return HttpResponse("ok")
		else:
			print "No existe una peticion"
			#response = JsonResponse({'aceptado':"False"})
			#return HttpResponse(response.content)
			return HttpResponse("No existe una peticion")
	else:
		return HttpResponseRedirect('NotFound');




"""
Autor: David Vinces
Nombre de funcion: aceptarComentario
Parametros: request, id de un comentario
Salida: 
Descripcion: cambia el estado de un comentario de una oferta para que sea visible
"""
@login_required
def aceptarComentario(request, id_comentario):
	try:
		comentario = ComentarioCalificacion.objects.get(id_comentario_calificacion = id_comentario)
		comentario.estado_comentario = 1
		oferta_id = comentario.fk_oferta.id_oferta
		comentario.save()
	except:
		return HttpResponseRedirect('/NotFound/')
	
	return HttpResponseRedirect('/administrarOferta/'+str(oferta_id))

"""
Autor: David Vinces
Nombre de funcion: rechazarComentario
Parametros: request, id de un comentario
Salida: 
Descripcion: cambia el estado de un comentario de una oferta para eliminarlo
"""
@login_required
def rechazarComentario(request, id_comentario):
	try:
		comentario = ComentarioCalificacion.objects.get(id_comentario_calificacion = id_comentario)
		comentario.estado_comentario=-1
		oferta_id = comentario.fk_oferta.id_oferta
		comentario.save()
	except:
		return HttpResponseRedirect('/NotFound/')
	
	return HttpResponseRedirect('/administrarOferta/'+str(oferta_id))

