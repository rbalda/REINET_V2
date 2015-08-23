from rest_framework.decorators import detail_route
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
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
    #parser_classes = (MultiPartParser,JSONParser)

    def get_queryset(self):
        busqueda = self.request.query_params.get('busqueda',None)
        print busqueda
        queryset = []
        usuario = Perfil.objects.get(id=self.request.user.id)
        if (busqueda != 'undefined') and (busqueda is not None):
            queryset = Oferta.objects.all().filter(publicada = 1, nombre__icontains=busqueda).exclude(miembroequipo__fk_participante=usuario.id_perfil).order_by('-fecha_publicacion')
        else:
            queryset = Oferta.objects.all().filter(publicada = 1).exclude(miembroequipo__fk_participante=usuario.id_perfil).order_by('-fecha_publicacion')
        return queryset


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
        busqueda = self.request.query_params.get('busqueda',None)
        print busqueda
        queryset = []
        usuario = Perfil.objects.get(id=self.request.user.id)
        if (busqueda != 'undefined') and (busqueda is not None):
            queryset = usuario.participa_en.all().filter(miembroequipo__es_propietario=1, publicada=1, nombre__icontains=busqueda).order_by('-fecha_publicacion')
        else:
            queryset = usuario.participa_en.all().filter(miembroequipo__es_propietario=1, publicada=1).order_by('-fecha_publicacion')
        return queryset


class MisOfertaBorradoresViewSet(ModelViewSet):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializador
    permission_classes = (IsAuthenticated,)
    lookup_field = 'codigo'
    pagination_class = PaginacionCinco

    def get_queryset(self):
        queryset = []
        busqueda = self.request.query_params.get('busqueda',None)
        usuario = Perfil.objects.get(id=self.request.user.id)
        #queryset = self.get_queryset().filter(miembroequipo__fk_participante=request.user.id, miembroequipo__es_propietario=1)
        if (busqueda != 'undefined') and (busqueda is not None):
            queryset = usuario.participa_en.all().filter(miembroequipo__es_propietario=1, publicada=0, nombre__icontains=busqueda).order_by('-fecha_creacion')
        else:
            queryset = usuario.participa_en.all().filter(miembroequipo__es_propietario=1, publicada=0).order_by('-fecha_creacion')
        return queryset

class MiembroOfertaViewSet(ModelViewSet):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializador
    permission_classes = (IsAuthenticated,)
    lookup_field = 'codigo'
    pagination_class = PaginacionCinco

    def get_queryset(self):
        busqueda = self.request.query_params.get('busqueda',None)
        queryset = []
        usuario = Perfil.objects.get(id=self.request.user.id)
        if (busqueda != 'undefined') and (busqueda is not None):
        #queryset = self.get_queryset().filter(miembroequipo__fk_participante=request.user.id, miembroequipo__es_propietario=1)
            queryset = usuario.participa_en.all().filter(miembroequipo__es_propietario=0, miembroequipo__estado_membresia=1, nombre__icontains=busqueda).order_by('-fecha_publicacion')
        else:
            queryset = usuario.participa_en.all().filter(miembroequipo__es_propietario=0, miembroequipo__estado_membresia=1).order_by('-fecha_publicacion')
        return queryset
