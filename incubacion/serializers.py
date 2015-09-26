from rest_framework.serializers import ModelSerializer
from datetime import date, datetime
from .models import Incubacion
from usuarios.models import Perfil

__author__ = 'faustomora'

# serializer de incubacion
class IncubacionSerializador(ModelSerializer):

    class Meta: # clase obligatoria, se define el modelo y los campos
        model = Incubacion
        fields = ('id_incubacion','nombre','descripcion','fecha_inicio','perfil_oferta','condiciones',
                    'tipos_oferta','otros','estado_incubacion','fk_perfil')
        read_only_fields = ('id_incubacion','otros','estado_incubacion','fk_perfil')


    # funcion para crear una incubacion
    def create(self,validated_data):
        
        # comando para crear una incubacion con el perfil del admin y los datos del validated data
        incubacion = Incubacion.objects.create(fk_perfil=Perfil.objects.get(id=self.context['request'].user.id),**validated_data)
        return incubacion