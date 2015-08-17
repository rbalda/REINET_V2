
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from ofertas_demandas.models import Oferta
from ofertas_demandas.models import Perfil
from ofertas_demandas.pagination import PaginacionPorDefecto
from ofertas_demandas.pagination import PaginacionCinco
from ofertas_demandas.pagination import NoPaginacion
from ofertas_demandas.permissions import SiEsPropietarioOEstaEnAlcance
from ofertas_demandas.serializers import OfertaSerializador
from rest_framework.response import Response

__author__ = 'rbalda'


class OfertaViewSet(ModelViewSet):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializador
    permission_classes = (IsAuthenticated,)
    lookup_field = 'codigo'
    pagination_class = PaginacionCinco

class MisOfertasAllViewSet(ModelViewSet):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializador
    permission_classes = (IsAuthenticated,)
    lookup_field = 'codigo'
    pagination_class = NoPaginacion

    def get_queryset(self):
        queryset = []
        usuario = Perfil.objects.get(id=self.request.user.id)
        queryset = usuario.participa_en.all().filter(miembroequipo__es_propietario=1)
        return queryset

class MisOfertaViewSet(ModelViewSet):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializador
    permission_classes = (IsAuthenticated,)
    lookup_field = 'codigo'
    pagination_class = PaginacionCinco

    def get_queryset(self):
        queryset = []
        usuario = Perfil.objects.get(id=self.request.user.id)
        #queryset = self.get_queryset().filter(miembroequipo__fk_participante=request.user.id, miembroequipo__es_propietario=1)
        queryset = usuario.participa_en.all().filter(miembroequipo__es_propietario=1, publicada=1)
        return queryset


class MisOfertaBorradoresViewSet(ModelViewSet):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializador
    permission_classes = (IsAuthenticated,)
    lookup_field = 'codigo'
    pagination_class = PaginacionCinco

    def get_queryset(self):
        queryset = []
        usuario = Perfil.objects.get(id=self.request.user.id)
        #queryset = self.get_queryset().filter(miembroequipo__fk_participante=request.user.id, miembroequipo__es_propietario=1)
        queryset = usuario.participa_en.all().filter(miembroequipo__es_propietario=1, publicada=0)
        return queryset

class MiembroOfertaViewSet(ModelViewSet):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializador
    permission_classes = (IsAuthenticated,)
    lookup_field = 'codigo'
    pagination_class = PaginacionCinco

    def get_queryset(self):
        queryset = []
        usuario = Perfil.objects.get(id=self.request.user.id)
        #queryset = self.get_queryset().filter(miembroequipo__fk_participante=request.user.id, miembroequipo__es_propietario=1)
        queryset = usuario.participa_en.all().filter(miembroequipo__es_propietario=0)
        return queryset

#aqui faltan unas cosas porque te mostrara todo pero vamos a hacer un ejemplo de como hacer una paginacion