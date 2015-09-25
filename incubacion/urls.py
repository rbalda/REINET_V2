from views import *
from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from incubacion import routers



urlpatterns = patterns('',
     url(r'^InicioIncubaciones[/]?$', 'incubacion.views.inicio_incubacion', name='InicioIncubacion'),
     url(r'^InicioIncubacion[/]?$', 'incubacion.views.ver_incubaciones', name='ver_incubaciones'),
     url(r'^CrearIncubacion[/]?$', 'incubacion.views.crear_incubacion', name='crear_incubacion'),
     url(r'^EditarMiIncubacion/(?P<incubacionid>(\d)+)[/]?$','incubacion.views.editar_mi_incubacion', name='editar_incubacion'),
     url(r'^AdminEditarEstadoIncubacion[/]?$','incubacion.views.editar_estado_incubacion', name='editar_estado_incubacion'),
     
     url(r'^AdminIncubacion/(?P<id_incubacion>\w{0,250})[/]?$', 'incubacion.views.admin_ver_incubacion',name='admin_ver_incubacion'),
     url(r'^VerIncubacion/(?P<id_incubacion>\w{0,250})[/]?$', 'incubacion.views.usuario_ver_incubacion',name='usuario_ver_incubacion'),
     url(r'^AdminIncubadasIncubacion[/]?$','incubacion.views.admin_incubadas_incubacion', name='admin_incubadas_incubacion'),
     url(r'^UsuarioIncubadasIncubacion[/]?$','incubacion.views.usuario_incubadas_incubacion', name='usuario_incubadas_incubacion'),
     url(r'^AdminSolicitudesIncubacion[/]?$','incubacion.views.admin_solicitudes_incubacion', name='admin_solicitudes_incubacion'),
     url(r'^RechazarSolicitudIncubacion[/]?$','incubacion.views.admin_rechazar_solicitud', name='admin_rechazar_solicitud'),
                       
     url(r'^BuscarConsultor[/]?$', 'incubacion.views.buscar_usuario', name='buscar_usuario'),
     url(r'^GuardarConvocatoria[/]?$', 'incubacion.views.guardar_convocatoria', name='guardar_convocatoria'),
     url(r'^VerMilestone/(?P<id_incubada>\w{0,250})[/]?$', 'incubacion.views.admin_ver_milestone', name='admin_ver_milestone'),
     url(r'^DefinirMilestone[/]?$', 'incubacion.views.definir_milestone', name='definir_milestone'),
     

     url(r'^AdminIncubada/(?P<id_oferta>\w{0,250})[/]?$','incubacion.views.admin_ver_incubada', name='admin_ver_incubada'),
     url(r'^AdminIncubadaConsultores[/]?$','incubacion.views.admin_incubada_consultores', name='admin_consultores'),
     url(r'^AdminIncubadaMilestoneActual[/]?$','incubacion.views.admin_incubada_milestone_actual', name='admin_incubada_milest_act'),
     url(r'^Retroalimentaciones[/]?$','incubacion.views.ver_retroalimentaciones', name='ver_retroalimentaciones'),
     url(r'^GuardarRetroalimentacion[/]?$','incubacion.views.guardar_retroalimentaciones', name='guardar_retroalimentaciones'),


     url(r'^ConsultorIncubada/(?P<id_oferta>\w{0,250})[/]?$', 'incubacion.views.consultor_ver_incubada',name='consultor_ver_incubada'),
     url(r'^Incubada/(?P<id_oferta>\w{0,250})[/]?$', 'incubacion.views.usuario_ver_incubada', name='usuario_ver_incubada'),

     url(r'^AutocompletarConsultor[/]?$', Autocompletar_Consultor.as_view(),name='AutocompletarConsultor'),
     url( r'^InivitarConsultor[/]?$', 'incubacion.views.invitar_consultor' , name = 'invitar_consultor' ),
     url( r'^ParticiparIncubacion[/]?$', 'incubacion.views.participar_incubacion' , name = 'participar_incubacion' ),
     url( r'^EnviarInvitaciones[/]?$', 'incubacion.views.enviar_invitaciones' , name = 'enviar_invitaciones' ),
     url(r'^EnviarOfertaParticipar[/]?$', 'incubacion.views.enviar_oferta_incubacion', name='enviar_oferta_incubacion'),
     url(r'^ContenidoMilestone[/]?$', 'incubacion.views.contenido_milestone', name='contenido_milestone'),
)


urlpatterns += routers.incubacion_routers
