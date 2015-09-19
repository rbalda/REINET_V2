from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Incubacion
from .serializers import IncubacionSerializador

__author__ = 'faustomora'


class IncubacionViewSet(ModelViewSet):
    queryset = Incubacion.objects.all()
    serializer_class = IncubacionSerializador
    permission_classes = (IsAuthenticated,)
