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



from usuarios.models import *
from django.db.models import Avg


# Create your views here.

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
	args['usuario']=request.user
	args['es_admin']=request.session['es_admin']
	args['incubacion'] = None
	return render_to_response('admin_crear_incubacion.html',args)

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
	args['usuario']=request.user
	args['es_admin']=request.session['es_admin']
	return render_to_response('admin_editar_mi_incubacion.html',args)


"""
Autor: Estefania Lozano
Nombre de funcion: admin_ver_incubada
Parametros: request
Salida: 
Descripcion: Mostar template editar mi incubacion
"""

@login_required
def admin_ver_incubacion(request):
	args = {}
	args['usuario']=request.user
	args['es_admin']=request.session['es_admin']
	return render_to_response('admin_ver_incubacion.html',args)



"""
Autor: Estefania Lozano
Nombre de funcion: admin_ver_incubada
Parametros: request
Salida: 
Descripcion: Mostar template de la incubada para el administrador de la incubacion
"""

@login_required
def admin_ver_incubada(request):
	args = {}
	args['usuario']=request.user
	args['es_admin']=request.session['es_admin']
	return render_to_response('admin_ver_incubada.html',args)


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
	args['usuario']=request.user
	args['es_admin']=request.session['es_admin']
	return render_to_response('consultor_ver_incubada.html',args)

"""
Autor: Estefania Lozano
Nombre de funcion: ver_incubada
Parametros: request
Salida: 
Descripcion: Mostar template de la incubada para el dueño de la incubada
"""

@login_required
def usuario_ver_incubada(request):
	args = {}
	args['usuario']=request.user
	args['es_admin']=request.session['es_admin']
	return render_to_response('usuario_ver_incubada.html',args)




"""
Autor: Jose Velez
Nombre de funcion: buscar_usuario
Parametros: request
Salida: Muetra el formulario de crear una incubacion
Descripcion: En esta pagina se puede crear incubaciones para las diferentes ofertas
"""

@login_required
def buscar_usuario(request):
	sesion=request.session['id_usuario']
	usuario=User.objects.get(id=sesion)
	args = {}
	if request.method=='POST':
		consultor = request.POST['consultor']
		emisor=User.objects.get(id=sesion)
		if consultor == emisor:
			args['mensaje_alerta']="No te puedes auto-aisgnarte consultor"
		else:
			try:
				receptor_aux = User.objects.get(username=consultor)
				receptor=receptor_aux
				tipo_mensaje = 'usuario-usuario'
			except User.DoesNotExist:
				print 'No existe usuario'
	else:
		args['usuario']=usuario
		args['es_admin']=request.session['es_admin']
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
	args['usuario']=request.user
	args['es_admin']=request.session['es_admin']
	return render_to_response('admin_ver_milestone.html',args)



def vista_404(request):
    try:
        id_session=request.session['id_user']
    except:
        id_session=None
    args={}
    if id_session is not None:
        tipo404="inicio_view"
    else:
        tipo404="index"
    args['tipo404']=tipo404
    return render_to_response('404.html',args,context_instance=RequestContext(request))
