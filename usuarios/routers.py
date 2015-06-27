__author__ = 'rbalda'

from swampdragon import route_handler
from swampdragon.route_handler import ModelRouter
from usuarios.models import Mensaje
from usuarios.dragon_serializers import MensajeSerializer


class MensajeRouter(ModelRouter):
    route_name = 'mensaje-router'
    serializer_class = MensajeSerializer
    model = Mensaje

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])

    def get_query_set(self, **kwargs):
        return self.model.objects.all()


route_handler.register(MensajeRouter)
