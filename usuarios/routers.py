

__author__ = 'rbalda'

from swampdragon import route_handler
from swampdragon.route_handler import ModelRouter
from usuarios.models import Mensaje
from usuarios.dragon_serializers import MensajeSerializer


class MensajeRouter(ModelRouter):
    route_name = 'mensaje-router'
    serializer_class = MensajeSerializer
    model = Mensaje
    valid_verbs = ['subscribe','get_single','get_list','get_contador_mensajes']



    def get_object(self, **kwargs):
        return self.model.objects.all().first()


    def get_query_set(self, **kwargs):
        return self.model.objects.all()


    def get_contador_mensajes(self):
        count = len(self.model.objects.filter(leido=False))
        return count




route_handler.register(MensajeRouter)
