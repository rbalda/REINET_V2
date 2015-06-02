from __future__ import unicode_literals

from django.db import models


class Institucion(models.Model):
    idinstitucion = models.AutoField(db_column='idInstitucion', primary_key=True)
    nombre = models.CharField(unique=True, max_length=45)
    siglas = models.CharField(max_length=12)
    logo = models.TextField()
    descripcion = models.CharField(max_length=500)
    mision = models.CharField(max_length=500)
    ubicacion = models.CharField(max_length=45)
    web = models.CharField(max_length=45)
    recursosofrecidos = models.CharField(db_column='recursosOfrecidos', max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'Institucion'


class Membresia(models.Model):
    idmembresia = models.AutoField(db_column='idMembresia', primary_key=True)
    esadministrator = models.IntegerField(db_column='esAdministrator') 
    cargo = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=45)
    fecha = models.CharField(max_length=45)
    ippeticion = models.CharField(db_column='ipPeticion', max_length=45) 
    estado = models.IntegerField(blank=True, null=True)
    fkinstitucion = models.ForeignKey(Institucion, db_column='fkInstitucion')
    fkusuario = models.ForeignKey('Usuario', db_column='fkUsuario') 

    class Meta:
        db_table = 'Membresia'


class Mensaje(models.Model):
    idmensaje = models.AutoField(db_column='idMensaje', primary_key=True) 
    mensaje = models.CharField(max_length=1000)
    fecha = models.DateTimeField()
    asunto = models.CharField(max_length=45)
    fkemisor = models.ForeignKey('Usuario', db_column='fkEmisor') 
    fkreceptor = models.ForeignKey('Usuario', db_column='fkReceptor')  

    class Meta:
        db_table = 'Mensaje'


class Peticion(models.Model):
    idpeticion = models.AutoField(db_column='idPeticion', primary_key=True) 
    nombre = models.CharField(max_length=45)
    codigo = models.CharField(max_length=128)
    usado = models.IntegerField()
    fkusuario = models.ForeignKey('Usuario', db_column='fkUsuario')  

    class Meta:
        db_table = 'Peticion'


class Ubicacion(models.Model):
    idubicacion = models.AutoField(db_column='idUbicacion', primary_key=True)  
    pais = models.CharField(max_length=45)
    ciudad = models.CharField(max_length=45)
    abreviatura = models.CharField(max_length=45)

    class Meta:
        db_table = 'Ubicacion'


class Usuario(models.Model):
    idusuario = models.AutoField(db_column='idUsuario', primary_key=True) 
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    contrasenia = models.CharField(max_length=64)
    cedula = models.CharField(unique=True, max_length=10)
    foto = models.TextField()
    web = models.CharField(max_length=100)
    telefono = models.CharField(max_length=16)
    fecharegistro = models.DateTimeField(db_column='fechaRegistro') 
    ipregistro = models.CharField(db_column='ipRegistro', max_length=15)  
    reputacion = models.DecimalField(max_digits=4, decimal_places=0)
    estado = models.IntegerField()
    privacidad = models.CharField(max_length=11)
    fkubicacion = models.ForeignKey(Ubicacion, db_column='fkUbicacion') 

    class Meta:
        db_table = 'Usuario'
