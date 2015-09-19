from rest_framework.serializers import ModelSerializer
from datetime import date, datetime
from .models import Incubacion

__author__ = 'faustomora'

class IncubacionSerializador(ModelSerializer):

    class Meta:
        model = Incubacion
        fields = ('id_incubacion','nombre','descripcion','fecha_inicio','perfil_oferta','condiciones','tipos_oferta','otros')
        read_only_fields = ('id_incubacion','otros')


    def create(self,validated_data):

        incubacion = Incubacion.objects.create(**validated_data)
        return incubacion