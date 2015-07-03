

__author__ = 'rbalda'

from swampdragon import route_handler
from swampdragon.route_handler import ModelRouter
from usuarios.models import Mensaje, Notificacion
from usuarios.dragon_serializers import *


class MensajeRouter(ModelRouter):
    route_name = 'mensaje-router'
    serializer_class = MensajeSerializer
    model = Mensaje


    def get_object(self, **kwargs):
        a = self.model.objects.filter(fk_receptor__username=kwargs['username'],leido=False).last()
        print a
        return a

    def get_query_set(self, **kwargs):
        return self.model.objects.all()




route_handler.register(MensajeRouter)


# Class para notificacion 

class NotificacionSerializer(ModelRouter):
    route_name = 'notificacion-router'
    serializer_class = NotificacionSerializer
    model = Notificacion


    def get_object(self, **kwargs):
        a = self.model.objects.filter(fk_receptor__username=kwargs['username'],leido=False).last()
        print a
        return a


route_handler.register(NotificacionSerializer)