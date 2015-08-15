from rest_framework import permissions
from ofertas_demandas.models import Oferta, MiembroEquipo
from usuarios.models import Perfil

__author__ = 'rbalda'


class SiEsPropietarioOEstaEnAlcance(permissions.BasePermission):

    def has_object_permission(self,request,view,obj):
        perfil = Perfil.objects.get(id=request.user.id)
        if request.method in permissions.SAFE_METHODS:
            perfil_temporal = MiembroEquipo.objects.filter(fk_oferta_en_que_participa=obj,fk_participante=perfil).first()
            return perfil_temporal.activo & perfil_temporal.estado > 0
        return MiembroEquipo.objects.filter(fk_oferta_en_que_participa=obj,fk_participante=perfil).first().es_propietario