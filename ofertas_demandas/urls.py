from ofertas_demandas import routers
from views import *
from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
		url(r'^InicioOferta[/]?$','ofertas_demandas.views.ofertas', name='InicioOferta'),
		url(r'^CrearOferta[/]?$','ofertas_demandas.views.CrearOferta', name='CrearOferta'),
		url(r'^CrearOfertaForm1/$','ofertas_demandas.views.CrearOfertaForm1', name='CrearOfertaForm1'),
		url(r'^CrearOfertaForm2/$','ofertas_demandas.views.CrearOfertaForm2', name='CrearOfertaForm2'),
		url(r'^CrearOfertaForm3/$','ofertas_demandas.views.CrearOfertaForm3', name='CrearOfertaForm3'),
		url(r'^CrearOfertaForm4/$','ofertas_demandas.views.CrearOfertaForm4', name='CrearOfertaForm4'),
		url(r'^CrearOfertaForm5/$','ofertas_demandas.views.CrearOfertaForm5', name='CrearOfertaForm5'),

		url(r'^oferta[/]?$','ofertas_demandas.views.verCualquierOferta', name='verOferta'),
		url(r'^administrarOferta[/]?$','ofertas_demandas.views.administrar_Oferta', name='AdministrarOferta'),
		url(r'^administrarBorrador[/]?$','ofertas_demandas.views.administrar_Borrador', name='administrarBorrador'),
		url(r'^EditarBorrador[/]?$','ofertas_demandas.views.editar_borrador', name='EditarBorrador'),
		)

urlpatterns += routers.ofertas_routers