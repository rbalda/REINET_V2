from django.contrib.auth.models import User
from usuarios.models import Institucion, Perfil

__author__ = 'rbalda'

from rest_framework import serializers


class InstitucionSerializador(serializers.ModelSerializer):
    ciudad = serializers.StringRelatedField()
    class Meta:
        model=Institucion
        fields = ('id_institucion','logo','nombre','siglas','ciudad')
        read_only_fields = ('id_institucion','logo','nombre','siglas','ciudad')

class PerfilSerializador(serializers.ModelSerializer):
    fk_ciudad = serializers.StringRelatedField()
    class Meta:
        model=Perfil
        fields = ('id_perfil','first_name','last_name','foto','fk_ciudad','username')
        read_only_fields = ('id_perfil','first_name','last_name','foto','fk_ciudad','username')


class UsuarioSerializador(serializers.ModelSerializer):
    label = serializers.SerializerMethodField('getuser',read_only=True)

    class Meta:
        model = User
        fields = ('label','first_name','last_name','username')
        read_only_fields = ('label','first_name','last_name','username')

    def getuser(self,obj):
        return obj.first_name + ' ' + obj.last_name + '-' + obj.username


