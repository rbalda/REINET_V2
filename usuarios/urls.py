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
        url(r'^suspender_usuario[/]?$','usuarios.views.suspenderUsuario',name='suspenderUsuario'),
		url(r'^perfilUsuario[/]?$','usuarios.views.perfilUsuario', name='perfilUsuario'),
        url(r'^suscribirAInstitucion/$','usuarios.views.suscribirAInstitucion', name='suscribirAInstitucion'),
        url(r'^verificarSuscripcion/$','usuarios.views.verificarSuscripcion', name='verificarSuscripcion'),
        url(r'^buzonMembresias/$','usuarios.views.buzonMembresias', name='buzonMembresias'),
        url(r'^accionMembresia/$','usuarios.views.accionMembresia', name='accionMembresia'),


        url(r'^perfilInstitucion[/]?$', 'usuarios.views.perfilInstitucion', name='perfilInstitucion'),
        url(r'^envioSolicitud[/]?$','usuarios.views.registrarSolicitud', name="envio_solicitud"),
        url(r'^registro_institucion/(?P<codigo>\w{0,50})[/]?$',registro_institucion,name='index'),
        url(r'^verPeticiones[/]?$',verPeticiones,name='verPeticiones'),
        url(r'^aceptarPeticiones[/]?$',aceptarPeticiones,name='aceptarPeticiones'),

        url(r'^registro_usuario[/]?$',registro_usuario,name='index'),
    	url(r'^index[/]?$',index,name='index'),
    	url(r'^[/]?$',index,name='index'),
    	url(r'^verificar_codigo[/]?$',verificarCodigo,name='institucion'),
    	url(r'^TerminosCondiciones[/]?$','usuarios.views.ver_terminos_condiciones', name='TerminosCondiciones'),
    	url(r'^inicioUsuario[/]?$','usuarios.views.inicio',name='inicioUsuario'),
        url(r'^editar_usuario[/]?$', 'usuarios.views.editar_usuario' ,name='index'),
        url(r'^editarContrasena[/]?$', 'usuarios.views.editarContrasena' ,name='editarContrasena'),
        url(r'^enviarEmailPassword[/]?$','usuarios.views.enviarEmailPassword',name='enviarEmailPassword'),
        url(r'^csrf_failure[/]?$', 'usuarios.views.csrf_failure', name='csrf_failure'),
        url(r'^editar_perfil_institucion[/]?$', 'usuarios.views.modificarPerfilInstitucion', name='editarPerfilInstitucion'),

        url(r'^AdministrarMembresias[/]?$', 'usuarios.views.administrar_membresias', name='AdministrarMembresias'),
        url(r'^MiembrosInstitucion[/]?$', 'usuarios.views.miembros_institucion', name='MiembrosInstitucion'),

        url(r'^usuario/(?P<username>\w{0,250})[/]?$','usuarios.views.verCualquierUsuario', name='verUsuario'),
        
        url(r'^verificar_siglas[/]?$',verificar_siglas, name="verificar_username"),

        url(r'^verificar_username[/]?$',verificar_username, name="verificar_username"),
        url(r'^verificar_cedula[/]?$',verificar_cedula, name="verificar_cedula"),
        url(r'^verificar_email[/]?$',verificar_email, name="verificar_email"),
       
        url(r'^GenerarCodigo[/]?$', generar_codigo, name='GenerarCodigo'),
        url(r'^getCiudades[/]?$',obtenerCiudades,name='institucion'),
        url(r'^institucion/(?P<institucionId>\w{0,50})[/]?$', verPerfilInstituciones,name='institucion'),


        url(r'^api/buscar_institucion[/]?',InstitucionBusqueda.as_view(),name='buscar_institucion'),
        url(r'^api/buscar_usuario[/]?',PerfilBusqueda.as_view(),name='buscar_usuario'),
        url(r'^api/contar_no_leidos[/]?',NumeroMensajesNoLeidos.as_view(),name='contar_no_leidos'),
        url(r'^api/notificaciones_no_leidas[/]?',NumeroNotificacionesNoLeidos.as_view(),name='notificar_no_leidos'),


        url(r'^BandejaDeEntrada[/]?$', ver_bandeja_entrada, name='BandejaDeEntrada'),
        url(r'^BandejaDeEntradaInstitucion[/]?$', ver_bandeja_entrada_institucion, name='BandejaDeEntradaInstitucion'),
        url(r'^enviarMensaje[/]?$', enviarMensaje, name='enviarMensaje'),
        url(r'^enviarMensajeInstitucion[/]?$', enviarMensajeInstitucion, name='enviarMensajeInstitucion'),
        url(r'^verMensaje[/]?$', verMensaje, name='verMensaje'),
        url(r'^verMensajeEnviado[/]?$', verMensajeEnviado, name='verMensajeEnviado'),
        url(r'^mensajesEnviados[/]?$', mensajesEnviados, name='mensajesEnviados'),
        url(r'^mensajesEnviadosInstitucion[/]?$', mensajesEnviadosInstitucion, name='mensajesEnviadosInstitucion'),
        url(r'^eliminarMensajeRecibido[/]?$', eliminarMensajeRecibido, name='eliminarMensajeRecibido'),
        url(r'^eliminarMensajeEnviado[/]?$', eliminarMensajeEnviado, name='eliminarMensajeEnviado'),
        url(r'^AutocompletarUsuario[/]?$', AutocompletarUsuario.as_view() , name='AutocompletarUsuario'),

        url(r'^NotFound[/]?$', vista_404, name='vista_404'),
)
# url(regex=r'^check_cedula/(?P<cedula>\d+)/$',
# view=CedulaCheck.as_view(),
# name='check_cedula'),
