from rest_framework import permissions
from ofertas_demandas.models import Oferta

__author__ = 'rbalda'


class SiEsPropietarioOEstaEnAlcance(permissions.BasePermission):

    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return Oferta.objects.get(equipo__fk_participante__id=request.user.id,equipo__es_propietario=True).exists()