# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.db import models
from django.contrib.auth.models import User
from cities_light.models import City, Country
from swampdragon.models import SelfPublishModel
from usuarios.dragon_serializers import MensajeSerializer, NotificacionSerializer

"""
Autor: René Balda
Nombre de funcion: definir_ruta_imagen
Parametros: self,filename
Salida: string que devuelve el directorio con un nombre generico para guardar la imagen
Descripcion: obtiene la instancia de la clase donde se use y el nombre del archivo original,
			devuelve un pat componiendo el id de perfil con la fecha de registro y aniade al nombre
			de la imagen un identificador que las va a diferenciar de acuerdo a la fecha, hora, y minuto
			que se subio la imagen
"""


def definir_ruta_imagen(self, filename):
    fecha_registro = self.date_joined.strftime("%Y%m%d")
    hoy = datetime.datetime.now().strftime("%Y%m%d%H%M")
    nombre_archivo_hoy = "%s_%s" % (hoy, filename)
    return "usuarios/%s%s/fotos/%s" % (self.id_perfil, fecha_registro, nombre_archivo_hoy)


def definir_ruta_imagen_institucion(self, filename):
    hoy = datetime.datetime.now().strftime("%Y%m%d%H%M")
    nombre_archivo_hoy = "%s_%s" % (hoy, filename)
    return "instituciones/%s%s/fotos/%s" % (self.siglas, self.id_institucion, nombre_archivo_hoy)


class Perfil(User):
    id_perfil = models.AutoField(primary_key=True)
    cedula = models.CharField(unique=True, max_length=10)
    foto = models.ImageField(upload_to=definir_ruta_imagen, default='noPicture.png')
    web = models.URLField(max_length=200)
    telefono = models.CharField(max_length=16)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ip_registro = models.GenericIPAddressField()
    reputacion = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    estado = models.PositiveSmallIntegerField(default=1)
    privacidad = models.SmallIntegerField(null=True, default=None)
    fk_ciudad = models.ForeignKey(City, related_name="ciudad_de_origen", default=None)
    fk_pais = models.ForeignKey(Country, related_name="pais_de_origen", default=None)
    actividades = models.TextField()

    class Meta:
        db_table = 'Perfil'


class Institucion(models.Model):
    id_institucion = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=45)
    siglas = models.CharField(max_length=12)
    logo = models.ImageField(upload_to=definir_ruta_imagen_institucion, default='noPicture.png')
    descripcion = models.CharField(max_length=500)
    mision = models.CharField(max_length=500)
    ciudad = models.ForeignKey(City, related_name="ciudad_origen", default=None)
    pais = models.ForeignKey(Country, related_name="pais_origen", default=None)
    web = models.CharField(max_length=45)
    recursos_ofrecidos = models.CharField(max_length=200, blank=True, null=True)
    miembros = models.ManyToManyField(User, through='Membresia', through_fields=('fk_institucion', 'fk_usuario'))
    correo = models.EmailField(default=None)
    telefono_contacto = models.CharField(max_length=15, default=None)

    class Meta:
        db_table = 'Institucion'


class Membresia(models.Model):
    id_membresia = models.AutoField(primary_key=True)
    es_administrator = models.BooleanField(default=False)
    cargo = models.CharField(max_length=45)
    descripcion_cargo = models.CharField(max_length=45)
    fecha_peticion = models.DateTimeField(auto_now_add=True)
    fecha_aceptacion = models.DateTimeField(default=None, null=True)
    ip_peticion = models.GenericIPAddressField(max_length=45)
    estado = models.SmallIntegerField(default=0)
    fk_institucion = models.ForeignKey(Institucion)
    fk_usuario = models.ForeignKey(User)

    class Meta:
        db_table = 'Membresia'


class Mensaje(SelfPublishModel, models.Model):
    id_mensaje = models.AutoField(primary_key=True)
    mensaje = models.CharField(max_length=1000)
    fecha_de_envio = models.DateTimeField()
    asunto = models.CharField(max_length=45)
    fk_emisor = models.ForeignKey(User, related_name='mensajes_enviados')
    fk_receptor = models.ForeignKey(User, related_name='mensajes_receptados')
    visible_emisor = models.BooleanField(default=True)
    visible_receptor = models.BooleanField(default=True)
    leido = models.BooleanField(default=False)
    serializer_class = MensajeSerializer


    def getReceptor(self):
        return self.fk_receptor

    user = property(getReceptor)

    def borrarMensaje(self):
        if not (self.visible_emisor or self.visible_receptor):
            self.delete()

    def imagenEmisor(self):
        try:
            p = Perfil.objects.get(user_ptr=self.fk_emisor)
            imagen = p.foto
            print "JAJAJA", imagen
        except:
            imagen = None
        return imagen

    imgEm = property(imagenEmisor)

    def imagenReceptor(self):
        try:
            p = Perfil.objects.get(user_ptr=self.fk_receptor)
            imagen = p.foto
            print "JAJAJA", imagen
        except:
            imagen = None
        return imagen

    imgRc = property(imagenReceptor)

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


class Notificacion(SelfPublishModel,models.Model):
    id_notificacion = models.AutoField(primary_key=True)
    estado_notificacion = models.BooleanField(default=False)
    destinatario_notificacion = models.ForeignKey(User)
    tipo_notificacion = models.TextField(max_length=50)
    descripcion_notificacion = models.TextField(max_length=150)
    url_notificacion = models.URLField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    serializer_class = NotificacionSerializer

    class Meta:
        db_table = 'Notificacion'

