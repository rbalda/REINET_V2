from swampdragon.serializers import model_serializer


__author__ = 'rbalda'
class MensajeContadorSerializador(model_serializer.ModelSerializer):
    class Meta:
        model = 'usuarios.Mensaje'
        publish_fields = ('asunto')

class MensajeSerializer(model_serializer.ModelSerializer):
    class Meta:
        model = 'usuarios.Mensaje'
        publish_fields = ('fk_emisor','asunto','mensaje')


