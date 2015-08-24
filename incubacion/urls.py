from views import *
from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
		url(r'^verIncubaciones[/]?$','incubacion.views.VerIncubaciones', name='VerIncubaciones'),
		url(r'^CrearIncubacion[/]?$','incubacion.views.crear_incubacion', name='crear_incubacion'),

		#url(r'^NotFound[/]?$', vista_404, name='NotFound'),
		)


