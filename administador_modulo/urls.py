from views import *
from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',

		url(r'^administrarUsuarios[/]?$','administador_modulo.views.administrar_usuarios', name='usuarios'),
		url(r'^adminrenderusuarios[/]?$','administador_modulo.views.usuarios_render', name='usuarios_render'),

)
