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
Nombre de funcion: InicioOferta
Parametros: request
Salida: 
Descripcion: para llamar la pagina oferta inicio
"""

@login_required
def VerIncubaciones(request):
	args = {}
	args['usuario']=request.user
	args['es_admin']=request.session['es_admin']
	return render_to_response('AdminIncVerIncubaciones.html',args)