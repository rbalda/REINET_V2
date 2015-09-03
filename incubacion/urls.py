from views import *
from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
		url(r'^InicioIncubacion[/]?$','incubacion.views.ver_incubaciones', name='ver_incubaciones'),
		url(r'^CrearIncubacion[/]?$','incubacion.views.crear_incubacion', name='crear_incubacion'),
        url(r'^VerIncubacion[/]?$','incubacion.views.ver_lista_incubadas', name='ver_incubadas'),
        url(r'^EditarMiIncubacion[/]?$','incubacion.views.editar_mi_incubacion', name='editar_incubacion'),
        url(r'^AdminIncubada[/]?$','incubacion.views.admin_ver_incubada', name='admin_ver_incubada'),
        url(r'^BuscarConsultor[/]?$', 'incubacion.views.buscar_usuario', name='buscar_usuario'),
		url(r'^VerMilestone[/]?$', 'incubacion.views.admin_ver_milestone', name='admin_ver_milestone'),       

		#url(r'^NotFound[/]?$', vista_404, name='NotFound'),
		)


