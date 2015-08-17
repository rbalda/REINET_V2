from ofertas_demandas import routers
from views import *
from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
		url(r'^InicioOferta[/]?$','ofertas_demandas.views.InicioOferta', name='InicioOferta'),
		url(r'^CrearOferta[/]?$','ofertas_demandas.views.CrearOferta', name='CrearOferta'),
		url(r'^CrearOfertaCopia[/]?$','ofertas_demandas.views.CrearOfertaCopia', name='CrearOfertaCopia'),
	

		url(r'^oferta/(?P<id_oferta>\w{0,250})[/]?$','ofertas_demandas.views.verCualquierOferta', name='verOferta'),
		url(r'^administrarOferta/(?P<id_oferta>\w{0,250})[/]?$','ofertas_demandas.views.administrar_Oferta', name='AdministrarOferta'),
		url(r'^administrarBorrador/(?P<id_oferta>\w{0,250})[/]?$','ofertas_demandas.views.administrar_Borrador', name='administrarBorrador'),
		url(r'^EditarBorrador/(?P<id_oferta>\w{0,250})[/]?$','ofertas_demandas.views.editar_borrador', name='EditarBorrador'),
        url(r'^equipoOferta[/]?$', 'ofertas_demandas.views.equipoOferta', name='equipoOferta'),
        url(r'^solicitarMembresiaOferta[/]?$', 'ofertas_demandas.views.solicitarMembresiaOferta', name='solicitarMembresiaOferta'),
		)

urlpatterns += routers.ofertas_routers
