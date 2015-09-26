import datetime
from django.db import models

# Create your models here.
from usuarios.models import Perfil, Institucion


def definir_ruta_imagen(self, filename):
    hoy = datetime.datetime.now().strftime("%Y%m%d%H%M")
    nombre_archivo_hoy = "%s_%s" % (hoy, filename)
    return "ofertas/%s/galeria/%s" % (self.fk_oferta.codigo, nombre_archivo_hoy)

def definir_ruta_imagen_demanda(self, filename):
    hoy = datetime.datetime.now().strftime("%Y%m%d%H%M")
    nombre_archivo_hoy = "%s_%s" % (hoy, filename)
    return "demandas/%s/galeria/%s" % (self.fk_demanda.codigo, nombre_archivo_hoy)

class DiagramaPorter(models.Model):
    id_diagrama_porter = models.AutoField(primary_key=True)
    competidores = models.TextField(blank=True)
    sustitutos = models.TextField(blank=True)
    consumidores = models.TextField(blank=True)
    proveedores = models.TextField(blank=True)
    nuevosMiembros = models.TextField(blank=True)

    class Meta:
        db_table = 'DiagramaPorter'


class DiagramaBusinessCanvas(models.Model):
    id_diagrama_business_canvas = models.AutoField(primary_key=True)
    asociaciones_clave = models.TextField(blank=True)
    actividades_clave = models.TextField(blank=True)
    recursos_clave = models.TextField(blank=True)
    propuesta_valor = models.TextField(blank=True)
    relacion_clientes = models.TextField(blank=True)
    canales_distribucion = models.TextField(blank=True)
    segmento_mercado = models.TextField(blank=True)
    estructura_costos = models.TextField(blank=True)
    fuente_ingresos = models.TextField(blank=True)

    class Meta:
        db_table = 'DiagramaBusinessCanvas'


class Oferta(models.Model):
    id_oferta = models.AutoField(primary_key=True)
    codigo = models.SlugField(unique=True)
    tipo = models.PositiveSmallIntegerField()
    estado = models.SmallIntegerField(default=1) # 1 para activa 2 para inactiva 3 para censurada
    nombre = models.CharField(max_length=300)
    publicada = models.BooleanField(default=False)
    calificacion_total = models.FloatField(default=0)
    descripcion = models.TextField()
    dominio = models.TextField()
    subdominio = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_publicacion = models.DateTimeField('Publicada',null=True,blank=True)
    tiempo_para_estar_disponible = models.CharField(max_length=25)
    perfil_beneficiario = models.TextField(null=True,blank=True)
    perfil_cliente = models.TextField(null=True,blank=True)
    descripcion_soluciones_existentes = models.TextField(null=True,blank=True)
    estado_propieada_intelectual = models.TextField(null=True,blank=True)
    evidencia_traccion = models.TextField(null=True,blank=True)
    cuadro_tendencias_relevantes = models.TextField(null=True,blank=True)
    fk_diagrama_competidores = models.OneToOneField(DiagramaPorter,related_name='oferta_con_este_diagrama_porter',null=True)
    fk_diagrama_canvas = models.OneToOneField(DiagramaBusinessCanvas,related_name='oferta_con_este_digrama_canvas',null=True)
    equipo = models.ManyToManyField(Perfil,through='MiembroEquipo',through_fields=('fk_oferta_en_que_participa','fk_participante'),related_name='participa_en')
    palabras_clave = models.ManyToManyField('PalabraClave',related_name='ofertas_con_esta_palabra')
    comentarios = models.ManyToManyField(Perfil,through='ComentarioCalificacion',through_fields=('fk_oferta','fk_usuario'),related_name='mis_comentarios')
    alcance = models.ManyToManyField(Institucion,related_name='ofertas_por_institucion')
    es_publica = models.BooleanField(default=False)#si es false el alcance de la oferta se tendra que validar con las intituciones asignadas
    
    class Meta:
        db_table = 'Oferta'
       # unique_together = ('id_oferta','codigo')
       # index_together = ['id_oferta','codigo']


class Demanda(models.Model):
    id_demanda = models.AutoField(primary_key=True)
    codigo = models.SlugField(unique=True)
    estado = models.PositiveSmallIntegerField() #Activo(1), Terminada(2), Desactiva(3) y Censurada(4)
    nombre = models.CharField(max_length=300)
    publicada = models.BooleanField(default=False)
    descripcion = models.TextField()
    dominio = models.TextField()
    subdominio = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_publicacion = models.DateTimeField('Publicada',null=True,blank=True)
    tiempo_para_estar_disponible = models.CharField(max_length=25)
    perfil_beneficiario = models.TextField(null=True,blank=True)
    perfil_cliente = models.TextField(null=True,blank=True)
    alternativas_soluciones_existentes = models.TextField(null=True,blank=True)
    lugar_donde_necesita = models.TextField(null=True,blank=True)
    importancia_resolver_necesidad = models.TextField(null=True,blank=True)
    fk_perfil = models.ForeignKey(Perfil)
    palabras_clave = models.ManyToManyField('PalabraClave',related_name='demandas_con_esta_palabra')
    alcance = models.ManyToManyField(Institucion,related_name='demandas_por_institucion')
    comentarios = models.ManyToManyField(Perfil,through='ComentarioDemanda',through_fields=('fk_demanda','fk_usuario'),related_name='usuarios_que_cpmentaron')
    es_publica = models.BooleanField(default=False)#si es false el alcance de la demanda se tendra que validar con las intituciones asignadas

    class Meta:
        db_table = 'Demanda'

class ResolucionDemanda(models.Model):
    id_propuesta = models.AutoField(primary_key=True)
    fk_oferta_demandante = models.ForeignKey(Oferta)
    fk_demanda_que_aplica = models.ForeignKey(Demanda)
    resuelve = models.SmallIntegerField(default=0)
    motivo = models.TextField()
    calificacion=models.SmallIntegerField(default=0)
    #-1 = no resuelve  0 = pendiente  1 = resuelve

    class Meta:
        db_table='ResolucionDemanda'

class MiembroEquipo(models.Model):
    id_equipo = models.AutoField(primary_key=True)
    fk_participante = models.ForeignKey(Perfil)
    fk_oferta_en_que_participa = models.ForeignKey(Oferta)
    es_propietario = models.BooleanField(default=False)
    rol_participante = models.TextField(default="Miembro del Equipo de la Oferta")
    activo = models.BooleanField(default=True)
    estado_membresia = models.SmallIntegerField(default=0) #si la membresia esta aceptada rechazada o pendiente
    fecha_aceptacion = models.DateTimeField(null=True,blank=True)
    comentario_peticion = models.TextField(null=True,blank=True)
    #0 = pendiente    1 = aceptada  -1 = rechazada
    class Meta:
        db_table='EquipoDeOferta'


class ImagenOferta(models.Model):
    id_imagen = models.AutoField(primary_key=True)
    imagen = models.ImageField(upload_to=definir_ruta_imagen)
    descripcion = models.TextField()
    fk_oferta = models.ForeignKey(Oferta,related_name='galeria')

    class Meta:
        db_table='ImagenOferta'

class ImagenDemanda(models.Model):
    id_imagen = models.AutoField(primary_key=True)
    imagen = models.ImageField(upload_to=definir_ruta_imagen_demanda)
    descripcion = models.TextField()
    fk_demanda = models.ForeignKey(Demanda,related_name='galeria')
    class Meta:
        db_table='ImagenDemanda'


class PalabraClave(models.Model):
    id_palabras_clave = models.AutoField(primary_key=True)
    palabra = models.CharField(max_length=20,unique=True)

    class Meta:
        db_table = 'PalabraClave'


class ComentarioCalificacion(models.Model):
    id_comentario_calificacion = models.AutoField(primary_key=True)
    comentario = models.TextField(null=True)
    calificacion = models.IntegerField(null=True)
    estado_comentario = models.SmallIntegerField(default=0)
    fecha_comentario = models.DateTimeField()
    fk_oferta = models.ForeignKey(Oferta)
    fk_usuario = models.ForeignKey(Perfil)

    class Meta:
        db_table= 'ComentarioCalificacionOferta'


class ComentarioDemanda(models.Model):
    id_comentario_calificacion = models.AutoField(primary_key=True)
    comentario = models.TextField(null=True)
    estado_comentario = models.SmallIntegerField(default=0)
    fecha_comentario = models.DateTimeField()
    fk_demanda = models.ForeignKey(Demanda)
    fk_usuario = models.ForeignKey(Perfil)

    class Meta:
        db_table= 'ComentarioDemanda'


