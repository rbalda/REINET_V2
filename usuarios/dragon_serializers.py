
from swampdragon.serializers import model_serializer


__author__ = 'rbalda'
# class UserSerializer(model_serializer.ModelSerializer):
#     class Meta:
#         model = 'django.contrib.auth.models.User'
#         publish_fields = ('username')

class MensajeSerializer(model_serializer.ModelSerializer):

    class Meta:
        model = 'usuarios.Mensaje'
        publish_fields = ('fk_emisor','asunto','mensaje','leido','fk_receptor')


# serializer para notificaciones
class NotificacionSerializer(model_serializer.ModelSerializer):

    class Meta:
        model = 'usuarios.Notificacion'
        #campos q se van a mostrar
        publish_fields = ('tipo_notificacion','descripcion_notificacion','estado_notificacion','destinatario_notificacion')


