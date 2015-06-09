from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from cities_light.models import City,Country

def get_upload_path(instance,filename):
        return 'usuarios/%s/fotos/%s'%(instance.user.id,filename)



class Perfil(User):
    id_perfil = models.AutoField(primary_key=True)
    cedula = models.CharField(unique=True, max_length=10)
    foto = models.ImageField(upload_to=get_upload_path,default='noPicture.png')
    web = models.URLField(max_length=200)
    telefono = models.CharField(max_length=16)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ip_registro = models.GenericIPAddressField()
    reputacion = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    estado = models.PositiveSmallIntegerField(default=1)
    privacidad = models.BinaryField(max_length=8)
    fk_ciudad = models.ForeignKey(City,related_name="ciudad_de_origen",default=None)
    fk_pais = models.ForeignKey(Country,related_name="pais_de_origen",default=None)
    actividades = models.TextField()

    class Meta:
        db_table = 'Perfil'


class Institucion(models.Model):
    id_institucion = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=45)
    siglas = models.CharField(max_length=12)
    logo = models.ImageField()
    descripcion = models.CharField(max_length=500)
    mision = models.CharField(max_length=500)
    ciudad = models.ForeignKey(City,related_name="ciudad_origen",default=None)
    pais = models.ForeignKey(Country,related_name="pais_origen",default=None)
    web = models.CharField(max_length=45)
    recursos_ofrecidos = models.CharField(max_length=200, blank=True, null=True)
    miembros = models.ManyToManyField(User,through='Membresia',through_fields=('fk_institucion','fk_usuario'))
    correo = models.EmailField(default=None)
    telefono_contacto = models.CharField(max_length=15,default=None )

    class Meta:
        db_table = 'Institucion'


class Membresia(models.Model):
    id_membresia = models.AutoField(primary_key=True)
    es_administrator = models.BooleanField(default=False)
    cargo = models.CharField(max_length=45)
    descripcion_cargo = models.CharField(max_length=45)
    fecha_peticion = models.DateTimeField(auto_now_add=True)
    fecha_aceptacion = models.DateTimeField(default=None)
    ip_peticion = models.GenericIPAddressField (max_length=45)
    estado = models.BooleanField(default=False)
    fk_institucion = models.ForeignKey(Institucion)
    fk_usuario = models.ForeignKey(User)

    class Meta:
        db_table = 'Membresia'


class Mensaje(models.Model):
    id_mensaje = models.AutoField(primary_key=True)
    mensaje = models.CharField(max_length=1000)
    fecha_de_envio = models.DateTimeField()
    asunto = models.CharField(max_length=45)
    fk_emisor = models.ForeignKey(User,related_name='mensajes_enviados')
    fk_receptor = models.ForeignKey(User,related_name='mensajes_receptados')

    class Meta:
        db_table = 'Mensaje'


class Peticion(models.Model):
    id_peticion = models.AutoField(primary_key=True)
    nombre_institucion = models.CharField(max_length=45)
    codigo = models.CharField(max_length=128)
    usado = models.BooleanField(default=False)
    fk_usuario = models.ForeignKey(User)

    class Meta:
        db_table = 'Peticion'

