__author__ = 'Ray'

from views import *
from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
        url(r'^registro_institucion[/]?$',registro_institucion,name='index'),

)