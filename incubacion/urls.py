from views import *
from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from incubacion import routers



urlpatterns = patterns('',
     url(r'^InicioIncubaciones[/]?$', 'incubacion.views.inicio_incubacion', name='InicioIncubacion'),
     url(r'^InicioIncubacion[/]?$', 'incubacion.views.ver_incubaciones', name='ver_incubaciones'),
     url(r'^CrearIncubacion[/]?$', 'incubacion.views.crear_incubacion', name='crear_incubacion'),
     url(r'^EditarMiIncubacion[/]?$', 'incubacion.views.editar_mi_incubacion',name='editar_incubacion'),
     url(r'^AdminIncubacion[/]?$', 'incubacion.views.admin_ver_incubacion',name='admin_ver_incubacion'),
     url(r'^AdminIncubada[/]?$', 'incubacion.views.admin_ver_incubada', name='admin_ver_incubada'),
     url(r'^BuscarConsultor[/]?$', 'incubacion.views.buscar_usuario', name='buscar_usuario'),
     url(r'^GuardarConvocatoria[/]?$', 'incubacion.views.guardar_convocatoria', name='guardar_convocatoria'),
     url(r'^VerMilestone[/]?$', 'incubacion.views.admin_ver_milestone', name='admin_ver_milestone'),

     url(r'^AdminIncubada/(?P<id_incubada>\w{0,250})[/]?$','incubacion.views.admin_ver_incubada', name='admin_ver_incubada'),
     url(r'^AdminConsultores[/]?$','incubacion.views.admin_consultores', name='admin_consultores'),
                       
     url(r'^ConsultorIncubada[/]?$', 'incubacion.views.consultor_ver_incubada',name='consultor_ver_incubada'),
     url(r'^Incubada[/]?$', 'incubacion.views.usuario_ver_incubada', name='usuario_ver_incubada'),

     url(r'^AutocompletarConsultor[/]?$', Autocompletar_Consultor.as_view(),name='AutocompletarConsultor'),

)


urlpatterns += routers.incubacion_routers
