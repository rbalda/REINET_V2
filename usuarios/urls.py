__author__ = 'Ray'

from views import *
from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',

		url(r'^logOut[/]?$','usuarios.views.logOut', name='logOut'),
		url(r'^signIn[/]?$','usuarios.views.signIn', name='signIn'),
		url(r'^autentificacion[/]?$','usuarios.views.autentificacion',name='autentificacion'),
		url(r'^signUp[/]?$','usuarios.views.signUp', name='signUp'),
		url(r'^perfilUsuario[/]?$','usuarios.views.perfilUsuario', name='perfilUsuario'),
        url(r'^registro_institucion[/]?$',registro_institucion,name='index'),
        url(r'^registro_usuario[/]?$',registro_usuario,name='index'),
    	url(r'^index[/]?$',index,name='index'),
    	url(r'^[/]?$',index,name='index'),
    	url(r'^ver_codigo[/]?$',verCodigo,name='institucion'),
    	url(r'^terms[/]?$','usuarios.views.terms', name='terms'),
)