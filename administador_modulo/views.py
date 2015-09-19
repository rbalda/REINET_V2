from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *

# Create your views here.


def administrar_usuarios(request):
	if request.method == "POST":
		pass
	else:
		args={}
		return render_to_response('administrar_usuarios.html', args)

"""
def usuarios_render(request):
	if request.method == "POST":
		print "entre"
		apellido=request.POST['apellido']
		print apellido
		usuarios=Perfil.objects.filter(last_name_icontains=apellido)
		print usuarios
		args={}
		args['usuarios']=usuarios
		return render_to_response('usuarios_render.html', args)
	else:
		print "else.."
		args={}
		return render_to_response('usuarios_render.html', args)
"""

def usuarios_render(request):
	try:
		print "entre"
		apellido=request.GET['apellido']
		print apellido
		usuarios_query=Perfil.objects.filter(last_name__icontains=apellido)
		paginator = Paginator(usuarios_query, 5) # Show 25 contacts per page
		page = request.GET.get('page')
		try:
			usuarios = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			usuarios = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			usuarios = paginator.page(paginator.num_pages)
		args={}
		args['usuarios']=usuarios
		return render_to_response('usuarios_render.html', args)
	except Exception as e:
		print e
		args={}
		return render_to_response('usuarios_render.html', args)
	
