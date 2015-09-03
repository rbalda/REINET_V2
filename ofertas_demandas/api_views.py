from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import detail_route
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from ofertas_demandas.models import Oferta, ImagenOferta
from ofertas_demandas.models import Perfil
from ofertas_demandas.models import PalabraClave
from ofertas_demandas.models import PalabraClave
from ofertas_demandas.models import *
from ofertas_demandas.pagination import PaginacionPorDefecto
from ofertas_demandas.pagination import PaginacionCinco
from ofertas_demandas.pagination import NoPaginacion
from ofertas_demandas.permissions import SiEsPropietarioOEstaEnAlcance
from ofertas_demandas.serializers import OfertaSerializador, DemandaSerializador
from rest_framework.response import Response
from usuarios.models import Institucion
from usuarios.serializers import InstitucionSerializador


__author__ = 'rbalda'


class AlcanceViewSet(ModelViewSet):
    queryset = Institucion.objects.all()
    serializer_class = DemandaSerializador
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = []
        queryset = Institucion.objects.all()
        return queryset

class DemandaViewSet(ModelViewSet):
    queryset = Demanda.objects.all()
    serializer_class = DemandaSerializador
    permission_classes = (IsAuthenticated,)
    pagination_class = PaginacionCinco
    def get_queryset(self):
        busqueda = self.request.query_params.get('busqueda',None)
        queryset = []
        usuario = Perfil.objects.get(id=self.request.user.id)
        if (busqueda != 'undefined') and (busqueda is not None):
            try: 
                queryset = PalabraClave.objects.all().filter(palabra = busqueda).first().demandas_con_esta_palabra.all().filter(publicada = 1).exclude(fk_perfil_id=usuario.id_perfil).order_by('-fecha_publicacion')
                queryset = queryset | Oferta.objects.all().filter(publicada = 1, nombre__icontains=busqueda).exclude(miembroequipo__fk_participante=usuario.id_perfil).order_by('-fecha_publicacion')
            except:
                queryset = Demanda.objects.all().filter(publicada = 1, nombre__icontains=busqueda).exclude(fk_perfil_id=usuario.id_perfil).order_by('-fecha_publicacion')
        else:
            queryset = Demanda.objects.all().filter(publicada = 1).exclude(fk_perfil_id=usuario.id_perfil).order_by('-fecha_publicacion')
        return queryset

class misDemandasAllViewSet(ModelViewSet):
    queryset = Demanda.objects.all()
    serializer_class = DemandaSerializador
    permission_classes = (IsAuthenticated,)
    pagination_class = PaginacionCinco

    def get_queryset(self):
        queryset = []
        usuario = Perfil.objects.get(id=self.request.user.id)
        queryset = Demanda.objects.all().filter(fk_perfil_id=usuario.id_perfil).order_by('-fecha_publicacion')
        return queryset


class MisDemandasViewSet(ModelViewSet):
    queryset = Demanda.objects.all()
    serializer_class = DemandaSerializador
    permission_classes = (IsAuthenticated,)
    pagination_class = PaginacionCinco

    def get_queryset(self):
        busqueda = self.request.query_params.get('busqueda',None)
        print busqueda
        queryset = []
        usuario = Perfil.objects.get(id=self.request.user.id)
        if (busqueda != 'undefined') and (busqueda is not None):
            queryset = Demanda.objects.all().filter(publicada = 1, fk_perfil_id=usuario.id_perfil, nombre__icontains=busqueda).order_by('-fecha_publicacion')
        else:
            queryset = Demanda.objects.all().filter(publicada = 1, fk_perfil_id=usuario.id_perfil).order_by('-fecha_publicacion')
        return queryset

class MisDemandasBorradoresViewSet(ModelViewSet):
    queryset = Demanda.objects.all()
    serializer_class = DemandaSerializador
    permission_classes = (IsAuthenticated,)
    pagination_class = PaginacionCinco

    def get_queryset(self):
        queryset = []
        busqueda = self.request.query_params.get('busqueda',None)
        usuario = Perfil.objects.get(id=self.request.user.id)
        #queryset = self.get_queryset().filter(miembroequipo__fk_participante=request.user.id, miembroequipo__es_propietario=1)
        if (busqueda != 'undefined') and (busqueda is not None):
            queryset = Demanda.objects.all().filter(publicada = 0, fk_perfil_id=usuario.id_perfil, nombre__icontains=busqueda).order_by('-fecha_publicacion')
        else:
            queryset = Demanda.objects.all().filter(publicada = 0, fk_perfil_id=usuario.id_perfil).order_by('-fecha_publicacion')
        return queryset

class OfertaViewSet(ModelViewSet):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializador
    permission_classes = (IsAuthenticated,)
    #lookup_field = 'codigo'
    pagination_class = PaginacionCinco
    #parser_classes = (MultiPartParser,JSONParser)

    def get_queryset(self):
        busqueda = self.request.query_params.get('busqueda',None)
        print busqueda
        queryset = []
        usuario = Perfil.objects.get(id=self.request.user.id)
        if (busqueda != 'undefined') and (busqueda is not None):
            try: 
                queryset = PalabraClave.objects.all().filter(palabra = busqueda).first().ofertas_con_esta_palabra.all().filter(publicada = 1).exclude(miembroequipo__fk_participante=usuario.id_perfil).order_by('-fecha_publicacion')
                queryset = queryset | Oferta.objects.all().filter(publicada = 1, nombre__icontains=busqueda).exclude(miembroequipo__fk_participante=usuario.id_perfil).order_by('-fecha_publicacion')
            except:
                queryset = Oferta.objects.all().filter(publicada = 1, nombre__icontains=busqueda).exclude(miembroequipo__fk_participante=usuario.id_perfil).order_by('-fecha_publicacion')
        else:
            queryset = Oferta.objects.all().filter(publicada = 1).exclude(miembroequipo__fk_participante=usuario.id_perfil).order_by('-fecha_publicacion')
        return queryset

    @detail_route(methods=['post'])
    def subir_imagen(self,request,pk=None):
        try:
            imagen = ImagenOferta()
            descripcion = self.request.DATA.get('descripcion',None)
            descripcion = descripcion.split(',')
            if descripcion:
                index = int(self.request.DATA['flowChunkNumber'])
                imagen.descripcion=descripcion[index-1]
            else:
                imagen.descripcion=" "

            id = self.request.DATA['id_oferta']
            imagen.fk_oferta = Oferta.objects.get(id_oferta=id)
            img = self.request.FILES['file']
            imagen.imagen = img
            imagen.save()
            return Response({'save_estado':True},status=status.HTTP_201_CREATED)
        except:
            return Response({'save_estado':False},status=status.HTTP_404_NOT_FOUND)


class MisOfertasAllViewSet(ModelViewSet):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializador
    permission_classes = (IsAuthenticated,)
    lookup_field = 'codigo'
    pagination_class = NoPaginacion

    def get_queryset(self):
        queryset = []
        usuario = Perfil.objects.get(id=self.request.user.id)
        queryset = usuario.participa_en.all().filter(miembroequipo__es_propietario=1).order_by('-fecha_publicacion')
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
