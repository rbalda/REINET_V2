from views import *
from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
		url(r'^InicioOferta[/]?$','ofertas_demandas.views.ofertas', name='InicioOferta'),
		url(r'^CrearOferta[/]?$','ofertas_demandas.views.crear_ofertas', name='CrearOferta'),
		url(r'^oferta[/]?$','ofertas_demandas.views.verCualquierOferta', name='verOferta'),
		url(r'^administrarOferta[/]?$','ofertas_demandas.views.administrar_miOferta', name='AdministrarOferta'),
		)