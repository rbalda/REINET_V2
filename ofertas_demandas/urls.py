from ofertas_demandas import routers
from views import *
from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
                       url(r'^InicioOferta[/]?$','ofertas_demandas.views.inicio_oferta', name='InicioOferta'),
                       url(r'^CrearOferta[/]?$','ofertas_demandas.views.crear_oferta', name='CrearOferta'),
                       url(r'^CrearOfertaCopia[/]?$','ofertas_demandas.views.crear_oferta_copia', name='CrearOfertaCopia'),
                       url(r'^CargarImagenOferta[/]?$','ofertas_demandas.views.cargar_imagen_oferta', name='CargarImagenOferta'),

                       url(r'^oferta/(?P<id_oferta>\w{0,250})[/]?$','ofertas_demandas.views.ver_cualquier_oferta', name='verOferta'),
                       url(r'^administrarOferta/(?P<id_oferta>\w{0,250})[/]?$','ofertas_demandas.views.administrar_Oferta', name='AdministrarOferta'),
                       url(r'^administrarBorrador/(?P<id_oferta>\w{0,250})[/]?$','ofertas_demandas.views.administrar_Borrador', name='administrarBorrador'),
                       url(r'^EditarBorrador/(?P<id_oferta>\w{0,250})[/]?$','ofertas_demandas.views.editar_borrador', name='EditarBorrador'),

                       url(r'^equipoOferta[/]?$', 'ofertas_demandas.views.equipoOferta', name='equipoOferta'),
                       url(r'^equipoEditableOferta[/]?$', 'ofertas_demandas.views.equipoEditableOferta', name='equipoOferta'),
                       url(r'^listaComentariosAceptados[/]?$', 'ofertas_demandas.views.listaComentariosAceptados', name='listaComentariosAceptados'),
                       #url(r'^editarEquipoOferta[/]?$', 'ofertas_demandas.views.editarEquipoOferta', name='editarEquipoOferta'),
                       url(r'^agregarParticipante[/]?$', 'ofertas_demandas.views.agregarParticipante', name='agregarParticipante'),
                       url(r'^AutocompletarParticipante[/]?$', AutocompletarParticipante.as_view() , name='AutocompletarParticipante'),

                       url(r'^solicitarMembresiaOferta[/]?$', 'ofertas_demandas.views.solicitarMembresiaOferta', name='solicitarMembresiaOferta'),
                       url(r'^publicarBorrador/(?P<id_oferta>\w{0,250})[/]?$','ofertas_demandas.views.publicar_borrador', name='publicarBorrador'),
                       url(r'^eliminarBorrador/(?P<id_oferta>\w{0,250})[/]?$','ofertas_demandas.views.eliminar_borrador', name='eliminarBorrador'),
                       url(r'^aceptarPeticionMiembro[/]?$','ofertas_demandas.views.aceptar_peticion', name='aceptar_peticion'),
                       url(r'^editarEstadoMembresia[/]?$','ofertas_demandas.views.editar_estado_membresia', name='editarEstadoMembresia'),
                       url(r'^editarRolMembresia[/]?$','ofertas_demandas.views.editar_rol_membresia', name='editarRolMembresia'),

                       url(r'^enviarComentario[/]?$', 'ofertas_demandas.views.enviarComentario', name='enviarComentario'),
                       url(r'^aceptarComentario/(?P<id_comentario>\w{0,250})[/]?$','ofertas_demandas.views.aceptarComentario', name='aceptarComentario'),
                       url(r'^rechazarComentario/(?P<id_comentario>\w{0,250})[/]?$','ofertas_demandas.views.rechazarComentario', name='rechazarComentario'),

                       url(r'^InicioDemanda[/]?$','ofertas_demandas.views.inicio_demanda', name='InicioDemanda'),
                       url(r'^CrearDemanda[/]?$','ofertas_demandas.views.crear_demanda', name='CrearDemanda'),
                       url(r'^CrearDemandaCopia[/]?$','ofertas_demandas.views.crear_demanda_copia', name='CrearDemandaCopia'),
                       url(r'^CargarImagenDemanda[/]?$','ofertas_demandas.views.cargar_imagen_demanda', name='CargarImagenDemanda'),
                       url(r'^EliminarBorradorDemanda/(?P<id_demanda>\w{0,250})[/]?$','ofertas_demandas.views.eliminar_borrador_demanda', name='EliminarBorradorDemanda'),

                       url(r'^demanda/(?P<id_demanda>\w{0,250})[/]?$','ofertas_demandas.views.ver_cualquier_demanda', name='verDemanda'),
                       url(r'^administrarDemanda/(?P<id_demanda>\w{0,250})[/]?$','ofertas_demandas.views.administrar_demanda', name='AdministrarDemanda'),
                       url(r'^listaComentariosAceptadosDemandas[/]?$', 'ofertas_demandas.views.listaComentariosAceptadosDemandas', name='listaComentariosAceptados'),
                       url(r'^enviarComentarioDemanda[/]?$', 'ofertas_demandas.views.enviarComentarioDemanda', name='enviarComentarioDemanda'),
                       url(r'^aceptarComentarioDemanda/(?P<id_comentario>\w{0,250})[/]?$','ofertas_demandas.views.aceptarComentarioDemanda', name='aceptarComentarioDemanda'),
                       url(r'^rechazarComentarioDemanda/(?P<id_comentario>\w{0,250})[/]?$','ofertas_demandas.views.rechazarComentarioDemanda', name='rechazarComentarioDemanda'),
                       url(r'^administrarBorradorDemanda/(?P<id_demanda>\w{0,250})[/]?$','ofertas_demandas.views.administrar_Borrador_Demanda', name='administrarBorrador'),
                       )

urlpatterns += routers.ofertas_routers
