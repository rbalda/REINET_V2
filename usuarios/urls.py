from views import *
from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

#Error 2 Revisar el estandar para mas informacion.
#Error 10 Revisar el estandar para mas informacion.

urlpatterns = patterns('',

		url(r'^cerrarSesion[/]?$','usuarios.views.cerrarSesion', name='cerrarSesion'),
		url(r'^iniciarSesion[/]?$','usuarios.views.iniciarSesion', name='iniciarSesion'),
        url(r'^recuperarPassword[/]?$','usuarios.views.recuperarPassword',name='recuperarPassword'),
        url(r'^suspender_usuario[/]?$',suspenderUsuario,name='suspenderUsuario'),
		url(r'^perfilUsuario[/]?$','usuarios.views.perfilUsuario', name='perfilUsuario'),
        url(r'^perfilInstitucion[/]?$', 'usuarios.views.perfilInstitucion', name='perfilInstitucion'),
        
        url(r'^SolicitudesInstitucion[/]?$', 'usuarios.views.mostrarMembresias', name='SolicitudesInstitucion'),
        url(r'^MiembrosInstitucion[/]?$', 'usuarios.views.mostrar_miembros_institucion', name='MiembrosInstitucion'),

        url(r'^envioSolicitud[/]?$','usuarios.views.registrarSolicitud', name="envio_solicitud"),
        url(r'^registro_institucion/(?P<codigo>\w{0,50})[/]?$',registro_institucion,name='index'),
        url(r'^verPeticiones[/]?$',verPeticiones,name='verPeticiones'),
        url(r'^aceptarPeticiones[/]?$',aceptarPeticiones,name='aceptarPeticiones'),

        url(r'^registro_usuario[/]?$',registro_usuario,name='index'),
    	url(r'^index[/]?$',index,name='index'),
    	url(r'^[/]?$',index,name='index'),
    	url(r'^verificar_codigo[/]?$',verificarCodigo,name='institucion'),
    	url(r'^terminosYcondiciones[/]?$','usuarios.views.terminosCondiciones', name='terminosYcondiciones'),
    	url(r'^inicioUsuario[/]?$','usuarios.views.inicio',name='inicioUsuario'),
        url(r'^editar_usuario[/]?$',editar_usuario,name='index'),
        url(r'^enviarEmailPassword[/]?$','usuarios.views.enviarEmailPassword',name='enviarEmailPassword'),
        url(r'^csrf_failure[/]?$', 'usuarios.views.csrf_failure', name='csrf_failure'),
        url(r'^editar_perfil_institucion[/]?$', 'usuarios.views.modificarPerfilInstitucion', name='editarPerfilInstitucion'),

        url(r'^usuario/(?P<username>\w{0,250})[/]?$','usuarios.views.verCualquierUsuario', name='verUsuario'),
        
        url(r'^verificar_username[/]?$',verificar_username, name="verificar_username"),
        url(r'^verificar_cedula[/]?$',verificar_cedula, name="verificar_cedula"),
        url(r'^verificar_email[/]?$',verificar_email, name="verificar_email"),
       
        url(r'^generarCodigo[/]?$', generarCodigo, name='generarCodigo'),
        url(r'^getCiudades[/]?$',obtenerCiudades,name='institucion'),
        url(r'^institucion/(?P<institucionId>\w{0,50})[/]?$', verPerfilInstituciones,name='institucion'),


        url(r'^api/buscar_institucion[/]?',InstitucionBusqueda.as_view(),name='buscar_institucion'),
        url(r'^api/buscar_usuario[/]?',PerfilBusqueda.as_view(),name='buscar_usuario'),

        url(r'^bandejaDeEntrada[/]?$', bandejaDeEntrada, name='bandejaDeEntrada'),
        url(r'^enviarMensaje[/]?$', enviarMensaje, name='enviarMensaje'),
        url(r'^verMensaje[/]?$', verMensaje, name='verMensaje'),
        url(r'^mensajesEnviados[/]?$', mensajesEnviados, name='mensajesEnviados'),
)
# url(regex=r'^check_cedula/(?P<cedula>\d+)/$',
# view=CedulaCheck.as_view(),
# name='check_cedula'),
