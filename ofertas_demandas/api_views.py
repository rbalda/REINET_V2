
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from ofertas_demandas.models import Oferta
from ofertas_demandas.pagination import PaginacionPorDefecto
from ofertas_demandas.permissions import SiEsPropietarioOEstaEnAlcance
from ofertas_demandas.serializers import OfertaSerializador

__author__ = 'rbalda'


class OfertaViewSet(ModelViewSet):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializador
    permission_classes = (IsAuthenticated,)
    lookup_field = 'codigo'
    pagination_class = PaginacionPorDefecto

