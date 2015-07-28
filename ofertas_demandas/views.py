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

"""
Autor: Leonel Ramirez
Nombre de funcion: ofertas
Parametros: request
Salida: 
Descripcion: para llamar la pagina oferta inicio
"""

@login_required
def ofertas(request):
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
def crear_ofertas(request):
	args = {}
	return render_to_response('crear_oferta.html',args)
