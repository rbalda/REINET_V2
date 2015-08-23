from views import *
from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
		url(r'^verIncubaciones[/]?$','incubacion.views.VerIncubaciones', name='VerIncubaciones'),

		)


