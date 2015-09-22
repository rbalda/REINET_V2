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
from datetime import *
from usuarios.serializers import InstitucionSerializador, PerfilSerializador, UsuarioSerializador

from incubacion.models import *
from incubacion.serializers import *

from usuarios.models import *
from django.db.models import Avg


# Create your views here.

"""
Autor: Kevin Zambrano
Nombre de funcion: inicio_incubacion
Parametros: request
Salida: render 
Descripcion: para llamar la pagina incubacion desde la barra de navegacion
"""
@login_required
def inicio_incubacion(request):
    args = {}
    args['usuario']=request.user
    args['es_admin']=request.session['es_admin']
    #Para el tab incubaciones de la red
    incubaciones = Incubacion.objects.all()
    args['incubaciones'] = incubaciones
    #Para el tab de incubadas
    incubadas = []
    for incubacion in incubaciones:
    	for incubada in  Incubada.objects.all():
    		if incubada.fk_incubacion.id_incubacion == incubacion.id_incubacion and incubacion.fk_perfil == request.user.perfil:
    			milestones = len(Milestone.objects.filter(fk_incubada = incubada))
    			consultores = len(incubada.consultores.all())
    			incubadas.append((incubada,milestones,consultores))
    args['incubadas'] = incubadas
    
    #Para el tab de consultores
    consultor = Consultor.objects.filter(fk_usuario_consultor= request.user.perfil)
    if consultor:
    	incubadas_consultores =  IncubadaConsultor.objects.filter(fk_consultor = consultor)
    	incubadas = []
    	for ic in incubadas_consultores:
            print ic.fk_incubada.id_incubada
            incubada = Incubada.objects.filter(id_incubada = ic.fk_incubada.id_incubada)
            if incubada:
                milestones = len(Milestone.objects.filter(fk_incubada = incubada))
                consultores=len(IncubadaConsultor.objects.filter(fk_incubada = incubada))
                incubadas.append((incubada, milestones, consultores))
        args['consultores'] = incubadas
    else:
		args['consultores'] = None

    return render_to_response('inicio_incubacion.html',args)

"""
Autor: Leonel Ramirez
Nombre de funcion: InicioIncubacion
Parametros: request
Salida: pagina de incubacion
Descripcion: para llamar la pagina incubacion inicio
"""
@login_required
def ver_incubaciones(request):
	args = {}
	args['usuario']=request.user
	args['es_admin']=request.session['es_admin']
	args['incubaciones'] = Incubacion.objects.filter(fk_perfil = request.user.perfil)
	return render_to_response('admin_incubacion_inicio.html',args)

"""
Autor: Jose Velez
Nombre de funcion: crear_incubacion
Parametros: request
Salida: Muetra el formulario de crear una incubacion
Descripcion: En esta pagina se puede crear incubaciones para las diferentes ofertas
"""
@login_required
def crear_incubacion(request):

    args = {}
    args['usuario'] = request.user
    args['es_admin'] = request.session['es_admin']

	# verificar que el creador de una incubacion sea admin de institucion
    if args['es_admin']: 
        return render_to_response('admin_crear_incubacion.html', args)

    # caso contrario no es admin y lo redirrecciona al inicio incubacion    
    else:
        return HttpResponseRedirect('InicioIncubaciones')


"""
Autor: Jose Velez
Nombre de funcion: invitar_consultor
Parametros: request
Salida: Muetra al usuario que desea invitar como consultor
Descripcion: En esta funcion mostrara los usuario que pueden ser consultor
"""
@login_required
def invitar_consultor(request):
    if request.is_ajax():

        q = request.GET.get( 'q' )
        usuario = q.split('-')
        print "Consultor: ",usuario[1]
        if q is not None:
            invitarConsultor = Perfil.objects.all()

            args['resultadosInvitarConsultores'] = invitarConsultor
            args.update(csrf(request))

            return render( request,'admin_invitar_consultor.html',args)
        else:
            print "No entro a consultor"

"""
Autor: Henry Lasso
Nombre de funcion: Editar_Incubacion
Parametros: request
Salida: 
Descripcion: Mostar template editar mi incubacion
"""


@login_required
def editar_mi_incubacion(request):
    args = {}
    args['usuario'] = request.user
    args['es_admin'] = request.session['es_admin']
    return render_to_response('admin_editar_mi_incubacion.html', args)


"""
Autor: Estefania Lozano
Nombre de funcion: admin_ver_incubada
Parametros: request
Salida: 
Descripcion: Mostar template editar mi incubacion
"""


@login_required
def admin_ver_incubacion(request,id_incubacion):
    session = request.session['id_usuario']
    usuario = Perfil.objects.get(id=session)
    args = {}
    args['es_admin']=request.session['es_admin']
    if usuario is not None:
        #Guardo en la variable de sesion a usuario.
        args['usuario'] = usuario
    else:
        args['error'] = "Error al cargar los datos"
        return HttpResponseRedirect('/NotFound/')
    incubacion = Incubacion.objects.get(id_incubacion=id_incubacion)
    convocatorias_incubacion = Convocatoria.objects.all().filter(fk_incubacion_id = id_incubacion).last()
    incubadas_incubacion = Incubada.objects.all().filter(fk_incubacion_id=id_incubacion)      
    #if convocatorias_incubacion.fecha_maxima

    args['incubacion'] = incubacion
    args['convocatorias'] = convocatorias_incubacion
    args['incubadas_incubacion'] = incubadas_incubacion    
    return render_to_response('admin_ver_incubacion.html', args)


"""
Autor: Estefania Lozano
Nombre de funcion: admin_ver_incubada
Parametros: request, id_incubada
Salida: Template admin_ver_incubada
Descripcion: Administrar una incubada de una incubacion de la cual soy dueño
"""
@login_required
def admin_ver_incubada(request,id_incubada):
    session = request.session['id_usuario']
    usuario = Perfil.objects.get(id=request.session['id_usuario'])
    args = {}
    args['es_admin']=request.session['es_admin']
    if usuario is not None:
        args['usuario'] = usuario
        try:
            incubada = Incubada.objects.get(id_incubada = id_incubada)
            #Tengo que verificar que el administrador de la incubada es el usuario en sesion
            if incubada.fk_incubacion.fk_perfil == usuario:
                propietario = MiembroEquipo.objects.get(id_equipo=incubada.equipo.id_equipo,es_propietario=1)
                equipo = MiembroEquipo.objects.get(id_equipo=incubada.equipo.id_equipo)
                if equipo is not None:
                    args['equipo'] = equipo
                args['incubada'] = incubada
                args['propietario'] = propietario
                return render_to_response('admin_ver_incubada.html', args)
            else:
                args['error'] = "Esta incubada no se encuentra bajo su administración"
                return HttpResponseRedirect('/NotFound/')
        #si la oferta no existe redirige a un mensaje de error
        except Incubada.DoesNotExist:
            args['error'] = "La incubada no se encuentra en la red, lo sentimos."
            return HttpResponseRedirect('/NotFound/')

    else:
        args['error'] = "Error al cargar los datos"
        return HttpResponseRedirect('/NotFound/')

"""
Autor: Estefania Lozano
Nombre de funcion: admin_consultores
Parametros: request
Salida: admin_lista_consultores
Descripcion: Esta funcion es para la peticion Ajax que pide mostrar la lista de consultores de la incubada
"""
@login_required
def admin_consultores(request):
    sesion = request.session['id_usuario']
    usuario = Perfil.objects.get(id=sesion)
    args = {}
    args['es_admin']=request.session['es_admin']
    #si el usuario EXISTE asigna un arg para usarlo en el template
    if usuario is not None:
        args['usuario'] = usuario
    else:
        args['error'] = "Error al cargar los datos"
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #si encuentra el ajax del template
    if request.is_ajax():
        try:
            #Debo obtener todos los consultores relacionados con la incubada, esto lo encuentro en la tabla incubadaConsultor
            incubConsult=IncubadaConsultor.objects.filter(fk_incubada=request.GET['incubada'])    
            #for c in incubConsult:
            #    try:
            #        print c.fk_consultor.fk_usuario_consultor.foto.url
            #    except Exception as e:
            #        print e
            args['consultores'] = incubConsult
            return render_to_response('admin_lista_consultores.html',args)

        except Incubada.DoesNotExist:
            print 'esa oferta no existe '
            return redirect('/')

        except IncubadaConsultor.DoesNotExist:
            print 'Este pana no tiene amigos :/'
            return redirect('/')

        except:
            print 'ya me jodi =('
            return redirect('/')

    else:
        return redirect('/NotFound')


"""
Autor: Estefania Lozano
Nombre de funcion: consultor_ver_incubada
Parametros: request
Salida: 
Descripcion: Mostar template de la incubada para el consultor de la incubada
"""


@login_required
def consultor_ver_incubada(request):
    args = {}
    args['usuario'] = request.user
    args['es_admin'] = request.session['es_admin']
    return render_to_response('consultor_ver_incubada.html', args)


"""
Autor: Estefania Lozano
Nombre de funcion: ver_incubada
Parametros: request
Salida: 
Descripcion: Mostar template de la incubada para el duenio de la incubada
"""


@login_required
def usuario_ver_incubada(request):
    args = {}
    args['usuario'] = request.user
    args['es_admin'] = request.session['es_admin']
    return render_to_response('usuario_ver_incubada.html', args)


"""
Autor: Jose Velez
Nombre de funcion: buscar_usuario
Parametros: request
Salida: Muetra el formulario de crear una incubacion
Descripcion: En esta pagina se puede crear incubaciones para las diferentes ofertas
"""


@login_required
def buscar_usuario(request):
    sesion = request.session['id_usuario']
    usuario = User.objects.get(id=sesion)
    args = {}
    if request.method == 'POST':
        consultor = request.POST['consultor']
        emisor = User.objects.get(id=sesion)
        if consultor == emisor:
            args['mensaje_alerta'] = "No te puedes auto-aisgnarte consultor"
        else:
            try:
                receptor_aux = User.objects.get(username=consultor)
                receptor = receptor_aux
                tipo_mensaje = 'usuario-usuario'
            except User.DoesNotExist:
                print 'No existe usuario'
    else:
        args['usuario'] = usuario
        args['es_admin'] = request.session['es_admin']
        args.update(csrf(request))


"""
Autor: Leonel Ramirez
Nombre de funcion: VerMilestone
Parametros: request
Salida: pagian ver milestone
Descripcion: para llamar la pagina ver milestone
"""


@login_required
def admin_ver_milestone(request):
    args = {}
    args['usuario'] = request.user
    args['es_admin'] = request.session['es_admin']
    return render_to_response('admin_ver_milestone.html', args)


class Autocompletar_Consultor(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.query_params.get('term', None)
        usuarios = User.objects.filter(username__icontains=user)[:5]
        serializador = UsuarioSerializador(usuarios, many=True)
        response = Response(serializador.data)
        return response


"""
Autor: Sixto Castro
Nombre de funcion: GuardarConvocatoria
Parametros: request
Salida: pagian ver milestone
Descripcion: para llamar la pagina ver milestone
"""

@login_required
def guardar_convocatoria(request):
    args = {}
    args['usuario'] = request.user
    args['es_admin'] = request.session['es_admin']

    """
        if args['es_admin']:
            if request.method == 'GET':
                fecha_max = request.GET['fecMaxima']
                id_incubacion = request.GET['idIncubacion']
                try:
                    convocatoria = Convocatoria()
                    convocatoria.fecha_creacion = datetime.datetime.now()
                    incubacion = Incubacion.objects.get(id_incubacion=id_incubacion)
                    convocatoria.fk_incubacion = incubacion
                    convocatoria.fecha_maxima = datetime.datetime.strptime(fecha_max, '%Y-%m-%d')
                    #convocatoria.fecha_maxima = fecha_max
                    if(convocatoria.fecha_maxima < convocatoria.fecha_creacion):
                        args['mensajeAlerta'] = 'Fecha maxima es menor a la actual'
                    else:
                        convocatoria.save()
                        convocatorias = Convocatoria.objects.all()
                        args['convocatorias'] = convocatorias

                        args['mensajeError'] = None
                        args['mensajeAlerta'] = 'Convocatoria Creada con exito'
                except ValueError:
                    print 'Error con la fecha'
                    args['mensajeError'] = 'La fecha tiene un formato errado. Debe ser (AAAA-MM-DD)'
                    args['mensajeAlerta'] = 'No se creo Convocatoria'
                    args.update(csrf(request))
                    return render_to_response('admin_ver_incubacion.html', args, context_instance=RequestContext(request))

            return render_to_response('admin_ver_incubacion.html', args)
        else:
            return HttpResponseRedirect('InicioIncubaciones')
    """
    return render_to_response('admin_ver_incubacion.html', args)
"""
Autor: Henry Lasso
Nombre de funcion: usuario_ver_incubacion
Parametros: request
Salida: 
Descripcion: Mostar template ver mi incubacion
"""


@login_required
def usuario_ver_incubacion(request,id_incubacion):
    session = request.session['id_usuario']
    usuario = Perfil.objects.get(id=session)
    args = {}
    args['es_admin']=request.session['es_admin']
    if usuario is not None:
        #Guardo en la variable de sesion a usuario.
        args['usuario'] = usuario
    else:
        args['error'] = "Error al cargar los datos"
        return HttpResponseRedirect('/NotFound/')
    incubacion = Incubacion.objects.get(id_incubacion=id_incubacion)
    
    args['incubacion'] = incubacion
    return render_to_response('usuario_ver_incubacion.html', args)

