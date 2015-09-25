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
Autor: Jose Velez
Nombre de funcion: definir_milestone
Parametros: request
Salida: Define un milestone a una incubada
Descripcion: Se define un milestone para que la incubada pueda cumplir con las retroalimentaciones
"""


@login_required
def definir_milestone(request):
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

    #Obtengo todos los datos del formulario para crear un Milestone
    requerimientos = request.GET.get( 'requerimientos' )
    fechaMilestone =  request.GET.get( 'fechaMilestone' )
    fechaRetroalimentacion = request.GET.get( 'fechaRetroalimentacion' )
    importancia =  request.GET.get( 'importancia' )
    otros = request.GET.get( 'otros' )
    idIncubada = request.GET.get( 'idIncubada' )
    fechaactual = datetime.datetime.now()

    #Modifico el formato de las fechas
    listaFM =fechaMilestone.split('/') 
    listaFR=fechaRetroalimentacion.split('/') 
    fechaMilestone = ""+listaFM[2]+"-"+listaFM[0]+"-"+listaFM[1]
    fechaRetroalimentacion = ""+listaFR[2]+"-"+listaFR[0]+"-"+listaFR[1]

    #Obtengo la incubada actual
    incubada_actual = Incubada.objects.get(id_incubada=idIncubada)

    #CLONO la incubada actual para crear un nuevo Milestone
    incubada_clonada = incubada_actual
    
    #ID OFERTA
    id_oferta= incubada_clonada.fk_oferta_id

    #ID DIAGRAMA DE CANVAS
    id_diagrama_canvas = incubada_actual.fk_diagrama_canvas_id
    #Obtengo el DIAGRAMA DE CANVAS
    canvas_incubada = DiagramaBusinessCanvas.objects.get(id_diagrama_business_canvas=id_diagrama_canvas)
    #CLONAR EL DIAGRAMA CANVAS
    canvas_clonado = canvas_incubada
    print "ID:       ",canvas_clonado.id_diagrama_business_canvas
    canvas_clonado.id_diagrama_business_canvas = None
    canvas_clonado.save()
    nuevo_id_diagrama_canvas = canvas_clonado.id_diagrama_business_canvas 
    print "ID:       ",nuevo_id_diagrama_canvas

    #ID DIAGRAMA PORTER
    id_diagrama_porter = incubada_actual.fk_diagrama_competidores_id
    #Obtengo el DIAGRAMA DE PORTER  
    porter_incubada = DiagramaPorter.objects.get(id_diagrama_porter=id_diagrama_porter)
    #CLONAR EL DIAGRAMA DE PORTER
    porter_clonado = porter_incubada
    print "ID PORTER:       ",porter_clonado.id_diagrama_porter
    porter_clonado.id_diagrama_porter = None
    porter_clonado.save()
    nuevo_id_diagrama_porter =  porter_clonado.id_diagrama_porter
    print "ID PORTER:       ",nuevo_id_diagrama_porter

    #Guardo los id de canvas y porter
    incubada_clonada.fk_diagrama_canvas_id = nuevo_id_diagrama_canvas
    incubada_clonada.fk_diagrama_competidores_id = nuevo_id_diagrama_porter
    print "ID INCUBADA ACTUAL:",incubada_clonada.id_incubada
    #Creando el codigo de la incubada con los atributos de idIncubada, idDiagramaCanvas, idDiagramaPorter
    incubada_clonada.codigo = incubada_clonada.id_incubada+nuevo_id_diagrama_canvas+nuevo_id_diagrama_porter
    incubada_clonada.id_incubada = None
    incubada_clonada.save()
    print "ID INCUBADA NUEVA:",incubada_clonada.id_incubada

    #Crea una instancia de Milestone
    milestone = Milestone()
    milestone.fecha_creacion = fechaactual
    milestone.fecha_maxima_Retroalimentacion = fechaRetroalimentacion
    milestone.fecha_maxima = fechaMilestone
    milestone.requerimientos = requerimientos
    milestone.importancia = importancia
    milestone.otros = importancia
    milestone.fk_incubada_id = incubada_clonada.id_incubada
    #milestone.save()
    print "MILESTONE GUARDADO"

"""
Autor: Leonel Ramirez 
Nombre de funcion: participar_incubacion
Parametros: request
Salida: Muetra al usuario que sus ofertas
Descripcion: En esta funcion mostrara las ofertas de un usuario para 
        participar a una incubacion
"""

@login_required
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
Nombre de funcion: contenido_milestone
Parametros: request
Salida: 
Descripcion: llama una funcion ajax para setear el contenido de cada milestone
"""

@login_required
def contenido_milestone(request):
    sesion = request.session['id_usuario']
    usuario = Perfil.objects.get(id=sesion)
    args = {}
    args['es_admin'] = request.session['es_admin']    
    #si el usuario EXISTE asigna un arg para usarlo en el template
    if usuario is not None:
        args['usuario'] = usuario
    else:
        args['error'] = "Error al cargar los datos"
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #si encuentra el ajax del template
    if request.is_ajax():
        print "Ingreso al ajax"
        try:
            #args['milestone'] = milestoneObjeto
            
            print "ID milestone:1111 "
            idMilestone = request.GET['milestoneId']
            milestone = Milestone.objects.get(id_milestone=idMilestone)
            incubada = milestone.fk_incubada

            
            print "ID milestone: 22222"
            if incubada:
                # Tengo que verificar que el administrador de la incubada es el usuario en sesion
                consultores = Consultor.objects.filter(fk_usuario_consultor=usuario.id_perfil)
                propietario = MiembroEquipo.objects.get(fk_oferta_en_que_participa=incubada.fk_oferta, es_propietario=1)
                
                if milestone:

                    #Validar que sea un administrador
                    if incubada.fk_incubacion.fk_perfil == usuario:
                                
                            #Ahora voy a buscar las palabras claves
                            palabras_Claves = incubada.palabras_clave.all()
                            if palabras_Claves.count() == 0:
                               palabras_Claves = False
                               args['palabras_clave'] = palabras_Claves

                            args['incubada'] = incubada
                            args['propietario'] = propietario
                            args['milestone'] = milestone
                            return render_to_response('contenido_historial_milestone.html', args)
                    
                    #Validar que sea un consultor                    
                    elif consultores:
                        consultor = Consultor.objects.get(fk_usuario_consultor=usuario.id_perfil)
                        incubadaCons=IncubadaConsultor.objects.filter(fk_consultor=consultor.id_consultor,fk_incubada=incubada.id_incubada)
                        if incubadaCons:
                            #Ahora voy a buscar las palabras claves
                            palabras_Claves = incubada.palabras_clave.all()
                            if palabras_Claves.count() == 0:
                               palabras_Claves = False
                               args['palabras_clave'] = palabras_Claves

                            args['incubada'] = incubada
                            args['propietario'] = propietario
                            args['milestone'] = milestone
                            return render_to_response('contenido_historial_milestone.html', args)


                    #Validar que sea un propietario
                    elif propietario.fk_participante.id_perfil==usuario.id_perfil:
                        #Ahora voy a buscar las palabras claves
                            palabras_Claves = incubada.palabras_clave.all()
                            if palabras_Claves.count() == 0:
                               palabras_Claves = False
                               args['palabras_clave'] = palabras_Claves

                            args['incubada'] = incubada
                            args['propietario'] = propietario
                            args['milestone'] = milestone
                            return render_to_response('contenido_historial_milestone.html', args)


                    else:
                        args['error'] = "Esta incubada no se encuentra bajo su administración"
                        return HttpResponseRedirect('/NotFound/')

                else:
                    args['error'] = "Esta incubada no se encuentra bajo su administración"
                    return HttpResponseRedirect('/NotFound/')
            else:
                args['error'] = "Esta incubada no se encuentra bajo su administración"
                return HttpResponseRedirect('/NotFound/')

        except Milestone.DoesNotExist:
            print '>> Milestone no existe'
            return redirect('/')
        except Incubada.DoesNotExist:
            print '>> Incubada no existe'
            return redirect('/')
        except:
            print '>> Excepcion no controlada INVITAR CONSULTOR'
            return redirect('/')
    else:
        print "NO INGRESO A INVITAR"
        return redirect('/NotFound')



"""
Autor: Leonel Ramirez
Nombre de funcion: inviar_oferta_incubacion
Parametros: request
Salida: envia id_oferta y id_incubacion
Descripcion: Solictud para pertenecer a una incubacion
"""

@login_required
def enviar_oferta_incubacion(request):
    session = request.session['id_usuario']
    usuario = Perfil.objects.get(id=session)
    args = {}
    args['es_admin']=request.session['es_admin']
    #si el usuario EXISTE asigna un arg para usarlo en el template
    if usuario is not None:
        args['usuario'] = usuario
    else:
        args['error'] = "Error al cargar los datos"
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.is_ajax():
            print "oqqqqqqqqqqqqqqqqqqqqla"
            print request.GET['incubacion']
            print "que hubo"
            print request.GET['oferta']
            print "id convocatoria"
            print request.GET['convocatoria']
            idIncubacion = request.GET['incubacion']
            idOferta = request.GET['oferta']
            idConvocatoria = request.GET['convocatoria']
            solicitudDatos = SolicitudOfertasConvocatoria()
            #enviar datos a la tabla solicitud convocatoria
            solicitudDatos.estado_solicitud = 0
            solicitudDatos.fk_convocatoria_id = idConvocatoria
            solicitudDatos.fk_oferta_id = idOferta
            solicitudDatos.fk_incubacion_id = idIncubacion
            solicitudDatos.fecha_creacion = datetime.datetime.now()
            solicitudDatos.save()
            return render_to_response('usuario_ver_incubada.html',args)
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

    consultor = request.GET.get( 'consultor' )
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
Autor: Jose Velez
Nombre de funcion: enviar_invitaciones
Parametros: request
Salida: Se envia a solicitud a todos los usuario
Descripcion: En esta funcion se guarda en la base todos los usuario que seran consultor
"""
@login_required
def enviar_invitaciones(request):
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

    usuarioPerfil = request.GET.get( 'usuarioperfil' )
    
    idIncubada =  request.GET.get( 'idincubada' )
    incubada = Incubada.objects.get(id_incubada=idIncubada)
    idIncubacion = incubada.fk_incubacion.id_incubacion
    idoferta = incubada.fk_oferta.id_oferta
    fechaactual = datetime.datetime.now()

    consultor = Consultor.objects.filter(fk_usuario_consultor=usuarioPerfil).filter(
            incubadaconsultor=IncubadaConsultor.objects.filter(fk_oferta_incubada_id=idoferta))
    incubadaPropietario=perfil.participa_en.all().get(miembroequipo__es_propietario=1,id_oferta=idoferta)
    if len(consultor) > 0:
        print "EL USUARIO NO PUEDE SER CONSULTOR"
    elif len(consultor) == 0:
        consultorExiste = Consultor.objects.filter(fk_usuario_consultor=usuarioPerfil)
        print len(consultorExiste)
        print 'ya imprimi el len'
        if len(consultorExiste)==0:
            #Guardar en la tabla Consultor
            consultorTabla = Consultor()
            consultorTabla.fk_usuario_consultor_id = usuarioPerfil
            consultorTabla.fecha_creacion = fechaactual
            #se guardan los cambios
            consultorTabla.save()
            consultorExiste=consultorTabla
        else:
            consultorExiste=consultorExiste.first()
        #Guardar en la tabla Consultor
        incubadaconsultor = IncubadaConsultor()
        incubadaconsultor.fk_consultor_id = consultorExiste.id_consultor
        incubadaconsultor.fk_incubada_id = idIncubada
        incubadaconsultor.fecha_creacion = fechaactual
        incubadaconsultor.fk_oferta_incubada_id=idoferta
        incubadaconsultor.fk_incubacion_id=idIncubacion
        #se guardan los cambios
        incubadaconsultor.save()


"""
Autor: Dimitri Laaz
Nombre de funcion: editar_mi_incubacion
Parametros: 
request-> petición http
id -> identificador de la incubación a editar
Salida: Vista con formulario de edición
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
Autor: Dimitri Laaz
Nombre de funcion: editar_estado_incubacion
Parametros: 
request-> petición http
Salida: Codigo de exito de la operación
Descripcion: Cambia el estado de una incubacion por medio de Ajax
"""
@login_required
def editar_estado_incubacion(request):
    if request.is_ajax():
        try:
            args = {}
            # se recupera el identificador de la sesión actual
            sesion = request.session['id_usuario']
            #se obtiene el usuario de la sesión actual
            usuario = Perfil.objects.get(id=sesion)
            #se recupera el id de la incubacion a cambiarle el estado
            incubacionid = request.GET.get("incubacion")
            #se recupera el nuevo estado a ser fijado
            estado_nuevo = request.GET.get("estado")
            # se valida que que el estado enviado tengo un valor valido
            estadoValido = re.search(u'^[12]$', estado_nuevo)
            if estadoValido is not None:
                try:
                    incubacion_cambiar = Incubacion.objects.get(id_incubacion=incubacionid)
                    #se valida que el usuario que solicita el cambio sea el dueño de la incubacion
                    if incubacion_cambiar.fk_perfil.id_perfil != usuario.id_perfil:
                        return HttpResponse(0)
                    #se valida que el estado actual sea activo para realizar el cambio
                    if incubacion_cambiar.estado_incubacion != 0:
                        return HttpResponse(1)
                    if incubacion_cambiar.estado_incubacion == 0:
                        #se realiza el cambio de estado si la condiciones son correctas
                        incubacion_cambiar.estado_incubacion = int(estado_nuevo)
                        incubacion_cambiar.save()
                        #se devuelve el codigo 2 de exito de la operacion
                        return HttpResponse(2)
                except ObjectDoesNotExist:
                    return HttpResponse(0)           
            else:
                return HttpResponse(3)         
        except:
            return HttpResponse(0)    
    return HttpResponseRedirect('/NotFound/')


"""
Autor: Henry Lasso
Nombre de funcion: admin_ver_incubacion
Parametros: request y id_incubacion
Salida: 
Descripcion: Mostar template ver mi incubacion desde administrador
"""

@login_required
def admin_ver_incubacion(request, id_incubacion):
    session = request.session['id_usuario']
    usuario = Perfil.objects.get(id=session)
    args = {}
    args['mensajeError'] = request.session['mensajeError']
    args['mensajeAlerta'] = request.session['mensajeAlerta']
    args['es_admin'] = request.session['es_admin']


    # Para que las variables de session sena colocadas en args[]
    if usuario is not None:
        args['usuario'] = usuario
        try:
            #obtengo la incubacion por medio del id enviado por la url
            incubacion = Incubacion.objects.get(id_incubacion=id_incubacion)
            #valido que el usuario sea dueño de la incubacion
            if incubacion.fk_perfil == usuario:    
                if incubacion:
                    #listo las convocatorias de la incubación
                    convocatorias_incubacion = Convocatoria.objects.all().filter(fk_incubacion_id=id_incubacion).last()
                    if convocatorias_incubacion is not None:
                        hoy = datetime.datetime.now(timezone.utc)
                        fecha_maxima = convocatorias_incubacion.fecha_maxima
                        # si la fecha maxima es menor a hoy no hay una convocatoria abierta
                        if fecha_maxima <= hoy:
                            args['convocatorias'] = "No hay Convocatoria"
                        else:
                            args['convocatorias'] = convocatorias_incubacion

                    else:
                        args['convocatorias'] = "No hay Convocatoria"

                    args['incubacion'] = incubacion
                    return render_to_response('admin_ver_incubacion.html', args)
                else:
                    args['error'] = "Esta incubada no se encuentra bajo su administración"
                    return HttpResponseRedirect('/NotFound/')
            else:
                args['error'] = "Esta incubacion no se encuentra bajo su administración"
                return HttpResponseRedirect('/NotFound/')
        except Incubacion.DoesNotExist:
            args['error'] = "La incubación no se encuentra en la red, lo sentimos."
            return HttpResponseRedirect('/NotFound/')
    else:
        args['error'] = "Error al cargar los datos"
        return HttpResponseRedirect('/NotFound/')

"""
Autor: Henry Lasso
Nombre de funcion: usuario_ver_incubacion
Parametros: request y id de incubacion
Salida: render template ver incubacion desde usuario 
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
        try:
            #obtengo la incubacion por medio del id 
            incubacion = Incubacion.objects.get(id_incubacion=id_incubacion)
            if incubacion :
                #listo la ultima convocatoria de la incubacion 
                convocatorias_incubacion = Convocatoria.objects.all().filter(fk_incubacion_id=id_incubacion).last()
                if convocatorias_incubacion is not None:
                    hoy = datetime.datetime.now(timezone.utc)
                    fecha_maxima = convocatorias_incubacion.fecha_maxima
                    # verifico si hay un convocatoria abierta por medio de las fechas
                    if fecha_maxima <= hoy:
                        args['convocatorias'] = "No hay Convocatoria"
                    else:
                        args['convocatorias'] = convocatorias_incubacion
                else:
                    args['convocatorias'] = "No hay Convocatoria"
                args['incubacion'] = incubacion
                return render_to_response('usuario_ver_incubacion.html', args)
            else:
                args['error'] = "Esta incubacion no se encuentra en la red"
                return HttpResponseRedirect('/NotFound/')
        except Incubacion.DoesNotExist:
            args['error'] = "La incubacion no se encuentra en la red, lo sentimos."
            return HttpResponseRedirect('/NotFound/')
    else:
        args['error'] = "Error al cargar los datos"
        return HttpResponseRedirect('/NotFound/')

"""
Autor: Henry Lasso
Nombre de funcion: admin_incubadas_incubacion
Parametros: request
Salida: admin_lista_incubadas desde administrador
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
            #obtengo las incubadas de la incubacion
            incubadas=Incubada.objects.all().filter(fk_incubacion_id = request.GET['incubacion'])
            imagenincubada = ImagenIncubada.objects.all().filter()
            propietarios = MiembroEquipo.objects.all().filter(es_propietario=1)
            if len(imagenincubada) > 0:
                args['imagenes']= imagenincubada
            else:
                 args['imagenes']= "No hay imagenes"   
            
            if len(incubadas) > 0:
                args['incubadas'] = incubadas
            else:    
                args['incubadas'] = "No hay incubadas"
            args['propietarios']= propietarios
            return render_to_response('admin_incubadas_de_incubacion.html',args)
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
Nombre de funcion: usuario_incubadas_incubacion
Parametros: request
Salida: usuario_lista_incubadas
Descripcion: Esta funcion es para la peticion Ajax que pide mostrar la lista de incubadas de la incubacion como usuario
"""

@login_required
def usuario_incubadas_incubacion(request):
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
            #obtengo las incubadas de la incubacion 
            incubadas=Incubada.objects.all().filter(fk_incubacion_id = request.GET['incubacion'])
            imagenincubada = ImagenIncubada.objects.all().filter()
            #obtengo todos los propietarios
            propietarios = MiembroEquipo.objects.all().filter(es_propietario=1)
            if len(imagenincubada) > 0:
                args['imagenes']= imagenincubada
            else:
                args['imagenes']= "No hay imagenes"   
            
            if len(incubadas) > 0:
                args['incubadas'] = incubadas
            else:    
                args['incubadas'] = "No hay incubadas"
            args['propietarios']= propietarios    
            return render_to_response('usuario_incubacion_incubadas.html',args)
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
    args['es_admin']=request.session['es_admin']
    #si el usuario EXISTE asigna un arg para usarlo en el template
    # si el usuario EXISTE asigna un arg para usarlo en el template
    if usuario is not None:
        args['usuario'] = usuario
    else:
        args['error'] = "Error al cargar los datos"
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #si encuentra el ajax del template
    if request.is_ajax():
        try:
            #obtengo todas las solicitudes de las convocatorias de la incubacion
            solicitudes = SolicitudOfertasConvocatoria.objects.all().filter(fk_incubacion = request.GET['incubacion'],estado_solicitud=0) 
            #obtengo todos los propietarios de la incubadas
            propietarios = MiembroEquipo.objects.all().filter(es_propietario=1)
            imagenesofertas = ImagenOferta.objects.all().filter()
            numeroimagenesoferta= len(imagenesofertas)
            if len(solicitudes) > 0:
                args['solicitudes'] = solicitudes
            else:    
                args['solicitudes'] = "No hay solicitudes"
            args['numeroimagenesoferta']=numeroimagenesoferta 
            args['imagenesofertas'] = imagenesofertas
            args['propietarios'] = propietarios
            return render_to_response('admin_incubacion_solicitudes.html',args)
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
Nombre de funcion: admin_rechazar_solicitud
Parametros: request
Salida: actualiza la solicitud con estado rechazada
Descripcion: Esta funcion es para la peticion Ajax que actualiza el estado de la solictud a rechazada
"""
@login_required
def admin_rechazar_solicitud(request):
    sesion = request.session['id_usuario']
    usuario = Perfil.objects.get(id=sesion)
    args = {}
    args['es_admin']=request.session['es_admin']
    #si el usuario EXISTE asigna un arg para usarlo en el template
    # si el usuario EXISTE asigna un arg para usarlo en el template
    if usuario is not None:
        args['usuario'] = usuario
    else:
        args['error'] = "Error al cargar los datos"
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #si encuentra el ajax del template
    if request.is_ajax():
        try:
            #obtengo las solicitudes pendientes de la incubacion
            solicitud= SolicitudOfertasConvocatoria.objects.get(id_solicitud_ofertas_convocatoria=request.GET['id_solicitud'])
            solicitud.estado_solicitud=2
            solicitud.save() 
        except:
            return redirect('/NotFound')
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
def admin_ver_incubada(request, id_oferta):
    session = request.session['id_usuario']
    usuario = Perfil.objects.get(id=request.session['id_usuario'])
    args = {}
    args['es_admin'] = request.session['es_admin']

    if usuario is not None:
        args['usuario'] = usuario
        try:
            incubada = Incubada.objects.filter(fk_oferta=id_oferta).last()
            # Tengo que verificar que el administrador de la incubada es el usuario en sesion
            if incubada:
                if incubada.fk_incubacion.fk_perfil == usuario:
                    propietario = MiembroEquipo.objects.get(fk_oferta_en_que_participa=incubada.fk_oferta, es_propietario=1)
                    equipo = MiembroEquipo.objects.filter(fk_oferta_en_que_participa=incubada.fk_oferta)
                    if len(equipo)>0:
                        args['equipo'] = equipo
                    fotos = ImagenIncubada.objects.filter(fk_incubada=incubada.id_incubada)
                    if fotos:
                        imagen_principal = fotos.first()
                    else:
                        fotos = False
                        imagen_principal = False

                    primer_Incubada = Incubada.objects.filter(fk_oferta=incubada.fk_oferta).first()
                    #Tenemos que validar si hay un mmilestone vigente
                    primer_milestone=Milestone.objects.filter(fk_incubada=primer_Incubada.id_incubada).first()
                    args['milestone']=primer_milestone


                    milestone = Milestone.objects.filter(fk_incubada=incubada.id_incubada).last()
                    if milestone:
                        hoy = datetime.datetime.now(timezone.utc)
                        fecha_maxima_milestone = milestone.fecha_maxima_Retroalimentacion

                        print 'hoolaaaaaaiisisdfjksafjaeefwer'
                        print hoy
                        print fecha_maxima_milestone
                        if fecha_maxima_milestone < hoy:
                            args['milestoneVigente'] = False
                        else:
                            args['milestoneVigente'] = True

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
                    return HttpResponseRedirect('/NotFound/')
            else:
                args['error'] = "Esta incubada no se encuentra bajo su administración"
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
            print 'chaaaaaaaaaaaaaaaaaaaaaaaaaaao'
            incubada = Incubada.objects.get(id_incubada=request.GET['incubada'])
            print 'hoooooooooooooooolaaaa'
            print incubada.fk_incubacion
            print incubada.fk_oferta
            consultores=IncubadaConsultor.objects.filter(fk_incubacion=incubada.fk_incubacion,fk_oferta_incubada=incubada.fk_oferta)
            #for c in incubConsult:
            #    try:
            #        print c.fk_consultor.fk_usuario_consultor.foto.url
            #    except Exception as e:
            #        print e
            args['consultores'] = consultores
            return render_to_response('consultores.html',args)

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
            milestone = Milestone.objects.filter(fk_incubada=request.GET['incubada']).last()

            hoy = datetime.datetime.now(timezone.utc)
            fecha_maxima_retroal = milestone.fecha_maxima_Retroalimentacion
            fecha_maxima_completar = milestone.fecha_maxima

            print hoy
            if fecha_maxima_retroal < hoy :
                print 'fecha maxima lalalalalalalar'
                print fecha_maxima_retroal
                args['retroalimentar']=False
                args['completar'] = False
                args['milestone'] = False
            elif fecha_maxima_completar <hoy and hoy<= fecha_maxima_retroal:
                print fecha_maxima_retroal,'fecha maxima retroalimentar'
                args['retroalimentar']=True
                args['completar'] = False
                args['milestone'] = milestone
            else:
                print fecha_maxima_completar,'fecha maxima completar'
                args['retroalimentar']=False
                args['completar'] = True
                args['milestone'] = milestone

            
            return render_to_response('milestone_actual.html',args)


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
    sesion = request.session['id_usuario']
    usuario = Perfil.objects.get(id=sesion)
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
                consultor = Consultor.objects.get(fk_usuario_consultor_id = usuario.id_perfil)
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
def consultor_ver_incubada(request,id_oferta):
    session = request.session['id_usuario']
    usuario = Perfil.objects.get(id=request.session['id_usuario'])
    args = {}
    args['es_admin']=request.session['es_admin']

    if usuario is not None:
        args['usuario'] = usuario
        try:
            incubada = Incubada.objects.filter(fk_oferta=id_oferta).last()
            #Tengo que verificar que el usuario es consultor de la incubada
            if incubada:
                consultores = Consultor.objects.filter(fk_usuario_consultor=usuario.id_perfil)
                if consultores:
                    consultor = Consultor.objects.get(fk_usuario_consultor=usuario.id_perfil)
                    incubadaCons=IncubadaConsultor.objects.filter(fk_consultor=consultor.id_consultor,fk_incubada=incubada.id_incubada)
                    if incubadaCons:
                        args['consultor']=usuario
                        propietario = MiembroEquipo.objects.get(fk_oferta_en_que_participa=incubada.fk_oferta, es_propietario=1)
                        equipo = MiembroEquipo.objects.filter(fk_oferta_en_que_participa=incubada.fk_oferta)
                        if len(equipo)>0:
                            args['equipo'] = equipo
                        fotos= ImagenIncubada.objects.filter(fk_incubada=incubada.id_incubada)
                        if fotos:
                            imagen_principal = fotos.first()
                        else:
                            fotos = False
                            imagen_principal = False

                        #Tenemos que encontrar el primer milestone que tuvo la oferta
                        primer_Incubada = Incubada.objects.filter(fk_oferta=incubada.fk_oferta).first()
                        primer_milestone=Milestone.objects.filter(fk_incubada=primer_Incubada.id_incubada).first()
                        args['milestone']=primer_milestone

                        #Ahora encontramos el milestone actual
                        milestone = Milestone.objects.filter(fk_incubada=incubada.id_incubada).last()
                        if milestone:
                            #lo siguiente es para validar que el consultor pueda retroalimentar
                            #Si es que el milestone ya fue completado pero no ha acabado el tiempo de retroalimentar
                            hoy = datetime.datetime.now(timezone.utc)
                            fecha_maxima_retro = milestone.fecha_maxima_Retroalimentacion
                            fecha_maxima_completar=milestone.fecha_maxima

                            if fecha_maxima_completar < hoy and hoy<=fecha_maxima_retro:
                                args['retroalimentar'] = True
                            else:
                                args['retroalimentar'] = False

                        #Ahora voy a buscar las palabras claves
                        palabras_Claves = incubada.palabras_clave.all()
                        if palabras_Claves.count()==0:
                            palabras_Claves=False
                        args['palabras_clave']=palabras_Claves

                        args['fotos'] = fotos
                        args['imagen_principal'] = imagen_principal
                        args['incubada'] = incubada
                        args['propietario'] = propietario
                        return render_to_response('consultor_ver_incubada.html', args)
                    else:
                        args['error'] = "El usuario no es consultor en esta incubada"
                        return HttpResponseRedirect('/NotFound/')  

                else:
                    args['error'] = "El usuario no es consultor en esta incubada"
                    return HttpResponseRedirect('/NotFound/')  
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
Nombre de funcion: ver_incubada
Parametros: request
Salida: 
Descripcion: Mostar template de la incubada para el duenio de la incubada
"""

@login_required
def usuario_ver_incubada(request,id_oferta):
    session = request.session['id_usuario']
    usuario = Perfil.objects.get(id=request.session['id_usuario'])
    args = {}
    args['es_admin']=request.session['es_admin']

    if usuario is not None:
        args['usuario'] = usuario
        try:
            incubada = Incubada.objects.filter(fk_oferta=id_oferta).last()
            #Tengo que verificar que el usuario es consultor de la incubada
            if incubada:
                print incubada.equipo.id_equipo
                propietario = MiembroEquipo.objects.get(fk_oferta_en_que_participa=incubada.fk_oferta, es_propietario=1)
                print 'propieeeeeeeeeeeeeeeeeeeeeeeetario'
                print propietario.fk_participante.id_perfil
                print 'usuaaaaaaaaaaaaaaaaariooooooooooooo'
                print usuario.id_perfil
                if propietario.fk_participante.id_perfil==usuario.id_perfil:

                    fotos= ImagenIncubada.objects.filter(fk_incubada=incubada.id_incubada)
                    if fotos:
                        imagen_principal = fotos.first()
                    else:
                        fotos = False
                        imagen_principal = False

                    equipo = MiembroEquipo.objects.filter(fk_oferta_en_que_participa=incubada.fk_oferta)
                    if len(equipo)>0:
                        args['equipo'] = equipo

                    #Tenemos que encontrar el primer milestone que tuvo la oferta
                    primer_Incubada = Incubada.objects.filter(fk_oferta=incubada.fk_oferta).first()
                    primer_milestone=Milestone.objects.filter(fk_incubada=primer_Incubada.id_incubada).first()
                    args['milestone']=primer_milestone

                    #Ahora encontramos el milestone actual
                    milestone = Milestone.objects.filter(fk_incubada=incubada.id_incubada).last()
                    if milestone:
                        #lo siguiente es para validar que el consultor pueda retroalimentar
                        #Si es que el milestone ya fue completado pero no ha acabado el tiempo de retroalimentar
                        hoy = datetime.datetime.now(timezone.utc)
                        fecha_maxima_retro = milestone.fecha_maxima_Retroalimentacion
                        fecha_maxima_completar=milestone.fecha_maxima

                        if fecha_maxima_completar < hoy and hoy<=fecha_maxima_retro:
                            args['completar'] = False
                            args['retroalimentar'] = True                            
                        elif fecha_maxima_completar > hoy:
                            args['completar'] = True
                            args['retroalimentar'] = False                            
                        else:
                            args['completar'] = False
                            args['retroalimentar'] = False 


                    #Ahora voy a buscar las palabras claves
                    palabras_Claves = incubada.palabras_clave.all()
                    if palabras_Claves.count()==0:
                        palabras_Claves=False
                    args['palabras_clave']=palabras_Claves

                    args['fotos'] = fotos
                    args['imagen_principal'] = imagen_principal
                    args['incubada'] = incubada
                    args['propietario'] = propietario
                    return render_to_response('usuario_ver_incubada.html', args)

                else:
                    args['error'] = "El usuario no es consultor en esta incubada"
                    return HttpResponseRedirect('/NotFound/')  
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
def admin_ver_milestone(request,id_incubada):
    args = {}
    args['usuario'] = request.user
    args['es_admin'] = request.session['es_admin']
    try:
        incubada=Incubada.objects.get(id_incubada=id_incubada)
        print incubada.fk_oferta
        args['incubada'] = incubada
        listaMilestone = Milestone.objects.all().filter()
        args['listaMilestone'] = listaMilestone
        return render_to_response('admin_ver_milestone.html', args)
    except Incubada.DoesNotExist:
        print '>> incubada no existe'
        return redirect('/NotFound/')
    except Exception as e:
        print e
        print '>> Excepcion no controlada ver milestone'
        return redirect('/NotFound/')

class Autocompletar_Consultor(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.query_params.get('term', None)
        usuarios = User.objects.filter(first_name__icontains=user)[:10]
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
                convocatoria.fecha_maxima = datetime.datetime.strptime(fecha_max, '%m/%d/%Y')
                # convocatoria.fecha_maxima = fecha_max
                if (convocatoria.fecha_maxima < convocatoria.fecha_creacion):
                    mensajeError = 'No se ha creado convocatoria dado que la fecha maxima es menor a la actual'
                    mensajeAlerta=None
                else:
                    convocatoria.save()
                    mensajeAlerta = 'Convocatoria Creada con exito'
                    mensajeError = None
            except:
                print 'Error con la fecha'
                mensajeError = 'No se creo Convocatoria. La fecha tiene un formato errado. Debe ser (MM/DD/AAAA)'
                mensajeAlerta = None

        request.session['mensajeError'] = mensajeError
        request.session['mensajeAlerta'] = mensajeAlerta
        return HttpResponseRedirect('AdminIncubacion/' + id_incubacion, args)
    else:
        return HttpResponseRedirect('InicioIncubaciones')



