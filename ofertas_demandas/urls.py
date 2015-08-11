from ofertas_demandas import routers
from views import *
from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
		url(r'^InicioOferta[/]?$','ofertas_demandas.views.InicioOferta', name='InicioOferta'),
		url(r'^CrearOferta[/]?$','ofertas_demandas.views.CrearOferta', name='CrearOferta'),
	

		url(r'^oferta[/]?$','ofertas_demandas.views.verCualquierOferta', name='verOferta'),
		url(r'^administrarOferta[/]?$','ofertas_demandas.views.administrar_Oferta', name='AdministrarOferta'),
		url(r'^administrarBorrador[/]?$','ofertas_demandas.views.administrar_Borrador', name='administrarBorrador'),
		url(r'^EditarBorrador[/]?$','ofertas_demandas.views.editar_borrador', name='EditarBorrador'),
		)

urlpatterns += routers.ofertas_routers