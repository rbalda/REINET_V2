

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
        a = self.model.objects.filter(fk_receptor__username=kwargs['username'],leido=False).order_by('fecha_de_envio').last()
        print a
        return a

    def get_query_set(self, **kwargs):
        return self.model.objects.all()




route_handler.register(MensajeRouter)


# Class para notificacion 

class NotificacionRouter(ModelRouter):
    route_name = 'notificacion-router'
    serializer_class = NotificacionSerializer
    model = Notificacion


    def get_object(self, **kwargs):
        a = self.model.objects.filter(destinatario_notificacion__username=kwargs['username'],estado_notificacion=False).order_by('fecha_creacion').last()
        print a
        return a

    def get_query_set(self, **kwargs):
        return self.model.objects.all()


route_handler.register(NotificacionRouter)