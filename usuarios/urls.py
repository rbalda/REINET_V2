from views import *
from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',

		url(r'^cerrarSesion[/]?$','usuarios.views.cerrarSesion', name='cerrarSesion'),
		url(r'^iniciarSesion[/]?$','usuarios.views.iniciarSesion', name='iniciarSesion'),
        url(r'^suspender_usuario[/]?$',suspenderUsuario,name='suspenderUsuario'),
		url(r'^perfilUsuario[/]?$','usuarios.views.perfilUsuario', name='perfilUsuario'),
        url(r'^perfilInstitucion[/]?$', 'usuarios.views.perfilInstitucion', name='perfilInstitucion'),
        url(r'^registro_institucion[/]?$',registro_institucion,name='index'),
        url(r'^registro_usuario[/]?$',registro_usuario,name='index'),
    	url(r'^index[/]?$',index,name='index'),
    	url(r'^[/]?$',index,name='index'),
    	url(r'^ver_codigo[/]?$',verificarCodigo,name='institucion'),
    	url(r'^terms[/]?$','usuarios.views.terms', name='terms'),
    	url(r'^inicioUsuario[/]?$','usuarios.views.inicio',name='inicioUsuario'),
        url(r'^editar_usuario[/]?$',editar_usuario,name='index'),
        url(r'^enviarEmailPassword[/]?$','usuarios.views.enviarEmailPassword',name='enviarEmailPassword'),
        url(r'^csrf_failure[/]?$', 'usuarios.views.csrf_failure', name='csrf_failure'),

        url(r'^generarCodigo[/]?$', generarCodigo, name='generarCodigo'),
        url(r'^getCiudades[/]?$',obtenerCiudades,name='institucion'),

)
# url(regex=r'^check_cedula/(?P<cedula>\d+)/$',
# view=CedulaCheck.as_view(),
# name='check_cedula'),
