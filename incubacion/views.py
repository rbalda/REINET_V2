# -*- encoding: utf-8 -*-
import random
import string
import re
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
from django.utils import timezone
from incubacion.models import *
from incubacion.serializers import *

from usuarios.models import *
from ofertas_demandas.models import *
from django.db.models import Avg


# Create your views here.

"""
Autor: Kevin Zambrano Cortez
Nombre de funcion: inicio_incubacion
Parametros: request
Salida: render 
Descripcion: para llamar la pagina incubacion desde la barra de navegacion
"""


@login_required
def inicio_incubacion(request):
    args = {}
    args['usuario'] = request.user
    args['es_admin'] = request.session['es_admin']
    # Para el tab incubaciones de la red
    incubaciones = Incubacion.objects.all()
    args['incubaciones'] = incubaciones
    #Para el tab de incubadas
    incubadas = []
    for incubacion in incubaciones:
        for incubada in Incubada.objects.all():
            if incubada.fk_incubacion.id_incubacion == incubacion.id_incubacion and incubacion.fk_perfil == request.user.perfil:
                milestones = len(Milestone.objects.filter(fk_incubada=incubada))
                consultores = len(incubada.consultores.all())
                incubadas.append((incubada, milestones, consultores))
    args['incubadas'] = incubadas

    #Para el tab de consultores
    consultor = Consultor.objects.filter(fk_usuario_consultor=request.user.perfil)
    if consultor:
        incubadas_consultores = IncubadaConsultor.objects.filter(fk_consultor=consultor)
        incubadas = []
        for ic in incubadas_consultores:
            incubada = Incubada.objects.filter(id_incubada=ic.fk_incubada.id_incubada)
            if incubada:
                milestones = len(Milestone.objects.filter(fk_incubada=incubada))
                consultores = len(IncubadaConsultor.objects.filter(fk_incubada=incubada))
                incubadas.append((incubada, milestones, consultores))
                print 'bsc'
                print incubadas
        args['consultores'] = incubadas
    else:
        args['consultores'] = None

    return render_to_response('inicio_incubacion.html', args)


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
    args['usuario'] = request.user
    request.session['mensajeError'] = None
    request.session['mensajeAlerta'] = None
    args['es_admin'] = request.session['es_admin']
    args['incubaciones'] = Incubacion.objects.filter(fk_perfil=request.user.perfil)
    return render_to_response('admin_incubacion_inicio.html', args)

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
Autor: Leonel Ramirez 
Nombre de funcion: participar_incubacion
Parametros: request
Salida: Muetra al usuario que sus ofertas
Descripcion: En esta funcion mostrara las ofertas de un usuario para 
        participar a una incubacion
"""


def participar_incubacion(request):
    sesion = request.session['id_usuario']
    usuario = Perfil.objects.get(id=sesion)
    args = {}
    args['es_admin'] = request.session['es_admin']
    # si el usuario EXISTE asigna un arg para usarlo en el template
    if usuario is not None:
        args['usuario'] = usuario
    else:
        args['error'] = "Error al cargar los datos"
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.is_ajax():
        try:
            #Obtener las ofertas del usuario actual
            #membresiaOferta = MiembroEquipo.objects.all().filter(fk_participante = usuario.id_perfil, fk_oferta_en_que_participa = id_oferta, es_propietario = 1).first()
            #oferta = Oferta.objects.filter(publicada=True)
            #ofertasusuario = MiembroEquipo.objects.filter(fk_participante = usuario.id_perfil, es_propietario = 1,)
            #f = MiembroEquipo.objects.filter(fk_participante = usuario.id_perfil, es_propietario = 1)
            ofertaParticipar = Oferta.objects.filter(publicada=1).filter(
                miembroequipo=MiembroEquipo.objects.filter(fk_participante=usuario.id_perfil, es_propietario=1))
            #ofer = MiembroEquipo.objects.filter(fk_participante=usuario.id_perfil, es_propietario=1).filter(oferta=Oferta.objects.filter(publicada = 1))
            #of1 = Oferta.objects.filter(id_oferta=of.fk_oferta_en_que_participa)
            #ofertasusuario = MiembroEquipo.objects.filter(oferta__in=oferta).select_related()
            print request.GET['incubacion']
            args['incubacion'] = request.GET['incubacion']
            args['pariciparIncubacion'] = ofertaParticipar
            return render_to_response('usuario_participar_incubacion.html', args)

        except Oferta.DoesNotExist:
            print '>> Oferta no existe'
            return redirect('/')
        except Exception as e:
            print e
            print '>> Excepcion no controlada PARTICIPAR INCUBACION'
            return redirect('/')
    else:
        return redirect('/NotFound')


"""
Autor: Leonel Ramirez
Nombre de funcion: inviar_oferta_incubacion
Parametros: request
Salida: envia id_oferta y id_incubacion
Descripcion: Solictud para pertenecer a una incubacion
"""


def enviar_oferta_incubacion(request):
    session = request.session['id_usuario']
    usuario = Perfil.objects.get(id=session)
    args = {}
    args['es_admin'] = request.session['es_admin']
    # si el usuario EXISTE asigna un arg para usarlo en el template
    if usuario is not None:
        args['usuario'] = usuario
    else:
        args['error'] = "Error al cargar los datos"
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.is_ajax():
        try:
            print "ola"
            print request.GET['incubacion']
            print "que hubo"
            print request.GET['oferta']
            return render_to_response('/usuario_ver_incubacion/', args)
        except Exception as e:
            print e
            print '>> Excepcion no controlada PARTICIPAR INCUBACION'
            return redirect('/')
        else:
            return redirect('/NotFound')
    else:
        return redirect('/NotFound')


"""
Autor: Jose Velez
Nombre de funcion: invitar_consultor
Parametros: request
Salida: Muetra al usuario que desea invitar como consultor
Descripcion: En esta funcion mostrara los usuario que pueden ser consultor
"""


@login_required
def invitar_consultor(request):
    sesion = request.session['id_usuario']
    usuario = Perfil.objects.get(id=sesion)
    args = {}
    args['es_admin'] = request.session['es_admin']
    # si el usuario EXISTE asigna un arg para usarlo en el template
    if usuario is not None:
        args['usuario'] = usuario
    else:
        args['error'] = "Error al cargar los datos"
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    consultor = request.GET.get('consultor')
    usuarioconsultor = consultor.split('-')
    if usuario.username == usuarioconsultor[1]:
        args['mismousuario'] = "NO SE PUEDE SELECCIONAR EL MISMO USUARIO"
    else:

        #si encuentra el ajax del template
        if request.is_ajax():
            try:
                print usuarioconsultor[1]
                invitarconsultor = Perfil.objects.get(username=usuarioconsultor[1])
                args['invitarconsultor'] = invitarconsultor
                print invitarconsultor
                return render_to_response('admin_invitar_consultor.html', args)

            except User.DoesNotExist:
                print '>> Usuario no existe'
                return redirect('/')
            except:
                print '>> Excepcion no controlada INVITAR CONSULTOR'
                return redirect('/')


        else:
            print "NO INGRESO A INVITAR"
            return redirect('/NotFound')

        return render_to_response('admin_invitar_consultor.html', args)


"""
Autor: Dimitri Laaz
Nombre de funcion: editar_mi_incubacion
Parametros: 
request-> petición http
id -> identificador de la incubación a editar
Salida: 
Descripcion: Carga los datos de una incubación para psoteriormente ser editada
"""


@login_required
def editar_mi_incubacion(request, incubacionid):
    try:
        args = {}
        # se recupera el identificador de la sesión actual
        sesion = request.session['id_usuario']
        #se obtiene el usuario de la sesión actual
        usuario = Perfil.objects.get(id=sesion)
        #se actualiza el token contra ataques de Cross Site Request Forgery(CSRF)
        args.update(csrf(request))

        #se envia el usuario y la bandera de administrador como argumentos de la vista
        args['usuario'] = request.user
        args['es_admin'] = request.session['es_admin']

        #se comprueba si la incubación solicitada existe
        try:
            incubacion_editar = Incubacion.objects.get(id_incubacion=incubacionid)
            if incubacion_editar.fk_perfil.id_perfil != usuario.id_perfil:
                return HttpResponseRedirect('/VerIncubacion/' + str(incubacion_editar.id_incubacion))
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/NotFound/')

        if request.method == 'POST':
            # se recuperan los datos enviados por medio de la peticion http POST
            nombreIncubacion = request.POST.get("nombre_incubacion")
            descripcionIncubacion = request.POST.get("descripcion_incubacion")
            perfilIncubacion = request.POST.get("perfil_incubacion")
            condicionesIncubacion = request.POST.get("condiciones_incubacion")
            tipoIncubacion = request.POST.get("select_tipo_incubacion")

            #validación de los campos por medio de expresiones regulares
            nombreValido = re.search(u'^([áéíóúÁÉÍÓÚñÑ\w]\s?){10,300}$', nombreIncubacion)
            descripcionValido = re.search(u'^([áéíóúÁÉÍÓÚñÑ\w]\s?[,;.:]?\s?)+$', descripcionIncubacion)
            perfilValido = re.search(u'^([áéíóúÁÉÍÓÚñÑ\w]\s?[,;.:]?\s?)+$', perfilIncubacion)
            condicionesValido = re.search(u'^([áéíóúÁÉÍÓÚñÑ\w]\s?[,;.:]?\s?)+$', condicionesIncubacion)
            tipoValido = re.search(u'^[012]$', tipoIncubacion)

            #se cambian los datos de la incubacion
            incubacion_editar.nombre = nombreIncubacion
            incubacion_editar.descripcion = descripcionIncubacion
            incubacion_editar.perfil_oferta = perfilIncubacion
            incubacion_editar.condiciones = condicionesIncubacion
            incubacion_editar.tipos_oferta = int(tipoIncubacion)

            #condicíon en caso de que un campo no este correcto
            if nombreValido is None or \
                            descripcionValido is None or \
                            perfilValido is None or \
                            condicionesValido is None or \
                            tipoValido is None:
                #se establece el mensaje de error de la operación
                args['errmsg'] = 1
                args['incubacion'] = incubacion_editar

                #se reenvia el formulario con los datos cambiados
                return render_to_response('admin_editar_mi_incubacion.html', args)


            #se guardan los cambios
            incubacion_editar.save()

            #Se establece el mensaje de éxito de la operación
            args['errmsg'] = 0

        #se envia la información de la incubación a la vista
        args['incubacion'] = incubacion_editar

        #se renderiza la vista
        return render_to_response('admin_editar_mi_incubacion.html', args)
    except:
        return redirect('/')


"""
Autor: Henry Lasso
Nombre de funcion: admin_ver_incubacion
Parametros: request
Salida: 
Descripcion: Mostar template ver mi incubacion
"""


@login_required
def admin_ver_incubacion(request, id_incubacion):
    session = request.session['id_usuario']
    usuario = Perfil.objects.get(id=session)
    args = {}
    args['es_admin'] = request.session['es_admin']

    # Para que las variables de session sena colocadas en args[]
    args['mensajeError'] = request.session['mensajeError']
    args['mensajeAlerta'] = request.session['mensajeAlerta']

    if usuario is not None:
        #Guardo en la variable de sesion a usuario.
        args['usuario'] = usuario
    else:
        args['error'] = "Error al cargar los datos"
        return HttpResponseRedirect('/NotFound/')

    incubacion = Incubacion.objects.get(id_incubacion=id_incubacion)
    convocatorias_incubacion = Convocatoria.objects.all().filter(fk_incubacion_id=id_incubacion).last()
    incubadas_incubacion = Incubada.objects.all().filter(fk_incubacion_id=id_incubacion)
    fecha_creacion = incubacion.fecha_inicio.strftime(' %d/%m/ %Y')
    if convocatorias_incubacion is not None:
        hoy = datetime.datetime.now(timezone.utc)
        print hoy
        fecha_maxima = convocatorias_incubacion.fecha_maxima
        if fecha_maxima <= hoy:
            print fecha_maxima
            args['convocatorias'] = "No hay Convocatoria"
        else:
            print hoy
            args['convocatorias'] = convocatorias_incubacion

    else:
        args['convocatorias'] = "No hay Convocatoria"

    args['incubacion'] = incubacion
    args['fecha_creacion'] = fecha_creacion
    args['incubadas_incubacion'] = incubadas_incubacion
    return render_to_response('admin_ver_incubacion.html', args)


"""
Autor: Henry Lasso
Nombre de funcion: admin_incubadas_incubacion
Parametros: request
Salida: admin_lista_incubadas
Descripcion: Esta funcion es para la peticion Ajax que pide mostrar la lista de incubadas de la incubacion
"""


@login_required
def admin_incubadas_incubacion(request):
    sesion = request.session['id_usuario']
    usuario = Perfil.objects.get(id=sesion)
    args = {}
    args['es_admin'] = request.session['es_admin']
    # si el usuario EXISTE asigna un arg para usarlo en el template
    if usuario is not None:
        args['usuario'] = usuario
    else:
        args['error'] = "Error al cargar los datos"
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #si encuentra el ajax del template
    if request.is_ajax():
        try:
            #Debo obtener todos los consultores relacionados con la incubada, esto lo encuentro en la tabla incubadaConsultor
            incubadas = Incubada.objects.all().filter(fk_incubacion_id=request.GET['incubacion'])
            pros = []
            if len(incubadas) > 0:
                args['incubadas'] = incubadas
                print "holaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                print incubadas
            else:
                args['incubadas'] = "No hay incubadas"
                print "cjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj"
                print len(incubadas)
            return render_to_response('admin_incubadas_de_incubacion.html', args)

        except Incubada.DoesNotExist:
            return redirect('/')
        except IncubadaConsultor.DoesNotExist:
            return redirect('/')
        except:
            return redirect('/')
    else:
        return redirect('/NotFound')


"""
Autor: Henry Lasso
Nombre de funcion: admin_solicitudes_incubacion
Parametros: request
Salida: admin_lista_solicitudes_incubacion
Descripcion: Esta funcion es para la peticion Ajax que pide mostrar la lista de ofertas aplicantes  a la incubacion
"""


@login_required
def admin_solicitudes_incubacion(request):
    sesion = request.session['id_usuario']
    usuario = Perfil.objects.get(id=sesion)
    args = {}
    args['es_admin'] = request.session['es_admin']
    # si el usuario EXISTE asigna un arg para usarlo en el template
    print "solicitudesssssssssssssssssssssss"
    if usuario is not None:
        args['usuario'] = usuario
    else:
        args['error'] = "Error al cargar los datos"
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #si encuentra el ajax del template
    if request.is_ajax():
        try:
            #Debo obtener todos los consultores relacionados con la incubada, esto lo encuentro en la tabla incubadaConsultor

            convocatoria = Convocatoria.objects.all().filter(fk_incubacion=request.GET['incubacion']).last()
            return render_to_response('admin_incubacion_solicitudes.html', args)
        except Incubada.DoesNotExist:
            return redirect('/')
        except IncubadaConsultor.DoesNotExist:
            return redirect('/')
        except:
            return redirect('/')
    else:
        return redirect('/NotFound')


"""
Autor: Estefania Lozano
Nombre de funcion: admin_ver_incubada
Parametros: request, id_incubada
Salida: Template admin_ver_incubada
Descripcion: Administrar una incubada de una incubacion de la cual soy dueño
"""


@login_required
def admin_ver_incubada(request, id_incubada):
    session = request.session['id_usuario']
    usuario = Perfil.objects.get(id=request.session['id_usuario'])
    args = {}
    args['es_admin'] = request.session['es_admin']

    if usuario is not None:
        args['usuario'] = usuario
        try:
            incubada = Incubada.objects.get(id_incubada=id_incubada)
            # Tengo que verificar que el administrador de la incubada es el usuario en sesion
            print incubada.fk_incubacion.fk_perfil
            if incubada:
                if incubada.fk_incubacion.fk_perfil == usuario:
                    propietario = MiembroEquipo.objects.get(id_equipo=incubada.equipo.id_equipo, es_propietario=1)
                    equipo = MiembroEquipo.objects.filter(id_equipo=incubada.equipo.id_equipo)
                    if equipo is not None:
                        args['equipo'] = equipo
                    fotos = ImagenIncubada.objects.filter(fk_incubada=id_incubada)
                    if fotos:
                        imagen_principal = fotos.first()
                    else:
                        fotos = False
                        imagen_principal = False

                    #Tenemos que validar si hay un mmilestone vigente
                    milestone = Milestone.objects.all().filter(fk_incubada=id_incubada).last()

                    if milestone:
                        hoy = datetime.datetime.now(timezone.utc)
                        fecha_maxima_milestone = milestone.fecha_maxima_Retroalimentacion

                        if fecha_maxima_milestone <= hoy:
                            args['ultimo_Milestone'] = milestone
                            milestone = False
                    else:
                        milestone = False
                    print milestone
                    args['milestone'] = milestone

                    #Ahora voy a buscar las palabras claves
                    palabras_Claves = incubada.palabras_clave.all()
                    if palabras_Claves.count() == 0:
                        palabras_Claves = False
                    args['palabras_clave'] = palabras_Claves

                    args['fotos'] = fotos
                    args['imagen_principal'] = imagen_principal
                    args['incubada'] = incubada
                    args['propietario'] = propietario
                    return render_to_response('admin_incubada.html', args)
            else:
                args['error'] = "Esta incubada no se encuentra bajo su administración"
                print "ingrese     30"
                return HttpResponseRedirect('/NotFound/')
        # si la oferta no existe redirige a un mensaje de error
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
def admin_incubada_consultores(request):
    sesion = request.session['id_usuario']
    usuario = Perfil.objects.get(id=sesion)
    args = {}
    args['es_admin'] = request.session['es_admin']
    # si el usuario EXISTE asigna un arg para usarlo en el template
    if usuario is not None:
        args['usuario'] = usuario
    else:
        args['error'] = "Error al cargar los datos"
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #si encuentra el ajax del template
    if request.is_ajax():
        try:
            #Debo obtener todos los consultores relacionados con la incubada, esto lo encuentro en la tabla incubadaConsultor
            incubConsult = IncubadaConsultor.objects.filter(fk_incubada=request.GET['incubada'])
            #for c in incubConsult:
            #    try:
            #        print c.fk_consultor.fk_usuario_consultor.foto.url
            #    except Exception as e:
            #        print e
            args['consultores'] = incubConsult
            return render_to_response('admin_incubada_consultores.html', args)

        except Incubada.DoesNotExist:
            return redirect('/')
        except IncubadaConsultor.DoesNotExist:
            return redirect('/')
        except:
            return redirect('/')
    else:
        return redirect('/NotFound')


"""
Autor: Estefania Lozano
Nombre de funcion: admin_incubada_milestone_actual
Parametros: request
Salida: ver admin_incubada_milestone_actual
Descripcion: Esta funcion es para la peticion Ajax que pide mostrar el milestone vigente en
    la vista de incubada para el administrador
"""


@login_required
def admin_incubada_milestone_actual(request):
    sesion = request.session['id_usuario']
    usuario = Perfil.objects.get(id=sesion)
    args = {}
    args['es_admin'] = request.session['es_admin']
    # si el usuario EXISTE asigna un arg para usarlo en el template
    if usuario is not None:
        args['usuario'] = usuario
    else:
        args['error'] = "Error al cargar los datos"
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #si encuentra el ajax del template
    if request.is_ajax():
        try:
            milestone = Milestone.objects.all().filter(fk_incubada=request.GET['incubada']).last()

            hoy = datetime.datetime.now(timezone.utc)
            fecha_maxima_milestone = milestone.fecha_maxima_Retroalimentacion

            if fecha_maxima_milestone <= hoy:
                milestone = False
            args['milestone'] = milestone

            return render_to_response('admin_incubada_milestone_actual.html', args)

        except Incubada.DoesNotExist:
            return redirect('/')
        except IncubadaConsultor.DoesNotExist:
            return redirect('/')
        except:
            return redirect('/')
    else:
        return redirect('/NotFound')


"""
Autor: Estefania Lozano
Nombre de funcion: ver_retroalimentaciones
Parametros: request
Salida: ver la lista de retroalimentaciones de cada tab de la incubada
Descripcion: Esta funcion es para la peticion Ajax que pide mostrar todas las retroalimentaciones 
    de cada tab
"""


@login_required
def ver_retroalimentaciones(request):
    sesion = request.session['id_usuario']
    usuario = Perfil.objects.get(id=sesion)
    args = {}
    args['es_admin'] = request.session['es_admin']
    # si el usuario EXISTE asigna un arg para usarlo en el template
    if usuario is not None:
        args['usuario'] = usuario
    else:
        args['error'] = "Error al cargar los datos"
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #si encuentra el ajax del template
    if request.is_ajax():
        try:
            id_incubada = request.GET['incubada']
            milestone = Milestone.objects.get(fk_incubada=id_incubada)
            numRetroal = 0
            if milestone:
                retroalimentaciones = Retroalimentacion.objects.filter(fk_milestone=milestone.id_milestone,
                                                                       num_tab=request.GET['numTab'])
                if retroalimentaciones:
                    numRetroal = retroalimentaciones.count()
            numTabVar = request.GET['numTab']

            args['idMilestone'] = milestone.id_milestone
            args['idIncubada'] = id_incubada
            args['numTabIncubada'] = numTabVar
            args['num_Retroal'] = numRetroal
            args['retroalimentaciones'] = retroalimentaciones
            return render_to_response('retroalimentaciones.html', args)

        except Incubada.DoesNotExist:
            return redirect('/')
        except:
            return redirect('/')
    else:
        return redirect('/NotFound')

"""
Autor: Sixto Castro
Nombre de funcion: guardar_retroalimentaciones
Parametros: request
Salida: ver la lista de retroalimentaciones de cada tab de la incubada
Descripcion: Esta funcion es para la peticion Ajax que pide mostrar todas las retroalimentaciones
    de cada tab
"""


@login_required
def guardar_retroalimentaciones(request):
    id_usuario = request.session['id_usuario']
    args = {}
    args['es_admin'] = request.session['es_admin']
    if args['es_admin']:
        if request.method == 'GET':
            num_tab = request.GET['numTab']
            id_incubada = request.GET['idIncubada']
            id_milestone = request.GET['idMilestone']
            contenido = request.GET['contenido']
            try:
                #print id_usuario
                retroalimentacion = Retroalimentacion()
                retroalimentacion.fecha_creacion = datetime.datetime.now()
                milestone = Milestone.objects.get(id_milestone=id_milestone)
                retroalimentacion.fk_milestone = milestone
                consultor = Consultor.objects.get(fk_usuario_consultor_id = id_usuario)
                retroalimentacion.fk_consultor = consultor
                retroalimentacion.contenido = contenido
                retroalimentacion.num_tab = num_tab
                retroalimentacion.save()
            except:
                print 'Error desconocido'

        return HttpResponseRedirect('AdminIncubada/' + id_incubada)
    else:
        return HttpResponseRedirect('InicioIncubaciones')


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
        usuarios = User.objects.filter(first_name__icontains=user)[:5]
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
                # convocatoria.fecha_maxima = fecha_max
                if (convocatoria.fecha_maxima < convocatoria.fecha_creacion):
                    mensajeAlerta = 'Fecha maxima es menor a la actual'
                else:
                    convocatoria.save()
                    mensajeAlerta = 'Convocatoria Creada con exito'
                mensajeError = None
            except:
                print 'Error con la fecha'
                mensajeError = 'La fecha tiene un formato errado. Debe ser (AAAA-MM-DD)'
                mensajeAlerta = 'No se creo Convocatoria'

        request.session['mensajeError'] = mensajeError
        request.session['mensajeAlerta'] = mensajeAlerta
        return HttpResponseRedirect('AdminIncubacion/' + id_incubacion, args)
    else:
        return HttpResponseRedirect('InicioIncubaciones')


"""
Autor: Henry Lasso
Nombre de funcion: usuario_ver_incubacion
Parametros: request
Salida: 
Descripcion: Mostar template ver mi incubacion
"""


@login_required
def usuario_ver_incubacion(request, id_incubacion):
    session = request.session['id_usuario']
    usuario = Perfil.objects.get(id=session)
    args = {}
    args['es_admin'] = request.session['es_admin']
    if usuario is not None:
        # Guardo en la variable de sesion a usuario.
        args['usuario'] = usuario
    else:
        args['error'] = "Error al cargar los datos"
        return HttpResponseRedirect('/NotFound/')

    incubacion = Incubacion.objects.get(id_incubacion=id_incubacion)
    convocatorias_incubacion = Convocatoria.objects.all().filter(fk_incubacion_id=id_incubacion).last()
    incubadas_incubacion = Incubada.objects.all().filter(fk_incubacion_id=id_incubacion)

    fecha_creacion = incubacion.fecha_inicio.strftime('%d de %b del %Y')
    if convocatorias_incubacion is not None:
        hoy = datetime.datetime.now(timezone.utc)
        print hoy
        fecha_maxima = convocatorias_incubacion.fecha_maxima
        if fecha_maxima <= hoy:
            print fecha_maxima
            args['convocatorias'] = "No hay Convocatoria"
        else:
            print hoy
            args['convocatorias'] = convocatorias_incubacion

    else:
        args['convocatorias'] = "No hay Convocatoria"
    args['incubacion'] = incubacion
    args['incubadas_incubacion'] = incubadas_incubacion
    args['fecha_creacion'] = fecha_creacion
    return render_to_response('usuario_ver_incubacion.html', args)

