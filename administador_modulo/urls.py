from views import *
from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',

		url(r'^gestionarUsuarios[/]?$','administador_modulo.views.administrar_usuarios', name='usuarios'),
		url(r'^adminrenderusuarios[/]?$','administador_modulo.views.usuarios_render', name='usuarios_render'),
		url(r'^gestionarOfertas[/]?$','administador_modulo.views.administrar_ofertas', name='usuarios'),
		url(r'^gestionarDemandas[/]?$','administador_modulo.views.administrar_demandas', name='usuarios'),
		
		url(r'^admin_render_ofertas[/]?$','administador_modulo.views.ofertas_render', name='usuarios_render'),
	url(r'^admin_render_demandas[/]?$','administador_modulo.views.demandas_render', name='usuarios_render'),
	url(r'^admin_editar_estado_demanda[/]?$','administador_modulo.views.admin_editar_estado_demanda', name='usuarios_render'),
	url(r'^admin_editar_estado_oferta[/]?$','administador_modulo.views.admin_editar_estado_oferta', name='usuarios_render'),
	url(r'^admin_editar_estado_usuario[/]?$','administador_modulo.views.admin_editar_estado_usuario', name='usuarios_render'),

	url(r'^verPeticiones[/]?$','administador_modulo.views.verPeticiones',name='verPeticiones'),
    url(r'^aceptarPeticiones[/]?$','administador_modulo.views.aceptarPeticiones',name='aceptarPeticiones'),


)
