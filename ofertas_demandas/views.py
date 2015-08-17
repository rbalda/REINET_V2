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
	#args['institucion_nombre'] = request.session['institucion_nombre']
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
			print 'lo logreee'
			args['listaEquipo'] = listaEquipo
			args['oferta']=oferta
			args.update(csrf(request))
			return render(request,'equipo_oferta.html',args)

		except Oferta.DoesNotExist:
			print 'esa oferta no existe BRONZA'
		except MiembroEquipo.DoesNotExist:
			print 'Este pana no tiene amigos :/'
		except:
			print 'ya me jodi =('
	else:
		return redirect('/NotFound')


"""
Autor: Ray Montiel
Nombre de la funcion: solicitarMembresiaOferta
Entrada:
Salida:
Descripción:Envia una solicitud para participar en una Oferta
"""
@login_required
def solicitarMembresiaOferta(request):
    if request.is_ajax():
        try:
            oferta = Oferta.objects.get(id_oferta=request.POST['oferta'])
            print request.POST['oferta']
            print request.user

            solicitudMembresia = MiembroEquipo.objects.get(fk_oferta_en_que_participa=oferta.id_oferta,fk_participante=request.user.id)

            if solicitudMembresia is not None and solicitudMembresia.estado==-1 :
                solicitudMembresia.rol_participante = "Miembro del Equipo de la Oferta"
                solicitudMembresia.estado_membresia = 0
                solicitudMembresia.save()
                print 'se actualizo parece'
                response = JsonResponse({'save_estado':True})
                return HttpResponse(response.content)

        except Oferta.DoesNotExist:
            print 'Oferta no existe'
        except MiembroEquipo.DoesNotExist:
                solicitudMembresia = MiembroEquipo()
                solicitudMembresia.es_propietario = False
                solicitudMembresia.rol_participante = "Miembro del Equipo de la Oferta"
                solicitudMembresia.estado_membresia = 0
                solicitudMembresia.fk_participante = request.user.perfil
                solicitudMembresia.fk_oferta_en_que_participa = oferta
                solicitudMembresia.save()
                print 'se guardo parece'
                response = JsonResponse({'save_estado':True})
                return HttpResponse(response.content)
    else:
        return redirect('/')



"""
Autor: Ray Montiel
Nombre de la funcion: verificaParticipacion
Entrada:
Salida:Habilita o inhabilita el boton de membresia
Descripción:Verifica que la solicitud para participar en una Oferta sea valida
"""

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