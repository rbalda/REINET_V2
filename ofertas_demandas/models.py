from django.db import models

# Create your models here.
from usuarios.models import Perfil


class DiagramaPorter(models.Model):
    id_diagrama_porter = models.AutoField(primary_key=True)
    competidores = models.TextField()
    sustitutos = models.TextField()
    consumidores = models.TextField()
    proveedores = models.TextField()
    nuevosMiembros = models.TextField()

    class Meta:
        db_table = 'DiagramaPorter'


class DiagramaBusinessCanvas(models.Model):
    id_diagrama_business_canvas = models.AutoField(primary_key=True)
    asociaciones_clave = models.TextField()
    actividades_clave = models.TextField()
    recursos_clave = models.TextField()
    propuesta_valor = models.TextField()
    relacion_clientes = models.TextField()
    canales_distribucion = models.TextField()
    segmento_mercado = models.TextField()
    estructura_costos = models.TextField()
    fuente_ingresos = models.TextField()

    class Meta:
        db_table = 'DiagramaBusinessCanvas'


class Oferta(models.Model):
    id_oferta = models.AutoField(primary_key=True)
    codigo = models.SlugField(unique=True)
    tipo = models.PositiveSmallIntegerField()
    nombre = models.CharField(max_length=300)
    publicada = models.BooleanField(default=False)
    calificacion_total = models.FloatField()
    descripcion = models.TextField()
    dominio = models.TextField()
    subdominio = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_publicacion = models.DateTimeField()
    tiempo_para_estar_disponible = models.DurationField()
    perfil_beneficiario = models.TextField()
    perfil_cliente = models.TextField()
    descripcion_soluciones_existentes = models.TextField(null=True)
    estado_propieada_intelectual = models.TextField(null=True)
    evidencia_traccion = models.TextField(null=True)
    cuadro_tendencias_relevantes = models.TextField()
    fk_diagrama_competidores = models.OneToOneField(DiagramaPorter,related_name='oferta_con_este_diagrama_porter')
    fk_diagrama_canvas = models.OneToOneField(DiagramaBusinessCanvas,related_name='oferta_con_este_digrama_canvas')
    equipo = models.ManyToManyField(Perfil,through='MiembroEquipo',through_fields=('fk_oferta_en_que_participa','fk_participante'),related_name='participa_en')
    palabras_clave = models.ManyToManyField('PalabraClave',related_name='ofertas_con_esta_palabra')
    comentarios = models.ManyToManyField(Perfil,through='ComentarioCalificacion',through_fields=('fk_oferta','fk_usuario'),related_name='mis_comentarios')


    class Meta:
        db_table = 'Oferta'
        unique_together = ('id_oferta','codigo')
        index_together = ['id_oferta','codigo']


class MiembroEquipo(models.Model):
    id_equipo = models.AutoField(primary_key=True)
    fk_participante = models.ForeignKey(Perfil)
    fk_oferta_en_que_participa = models.ForeignKey(Oferta)
    es_propietario = models.BooleanField(default=False)
    rol_participante = models.TextField()
    activo = models.BooleanField(default=True)
    estado_membresia = models.PositiveSmallIntegerField()

    class Meta:
        db_table='EquipoDeOferta'


class ImagenOferta(models.Model):
    id_imagen = models.AutoField(primary_key=True)
    imagen = models.ImageField()
    descripcion = models.TextField()
    fk_oferta = models.ForeignKey(Oferta,related_name='imagenes_oferta')

    class Meta:
        db_table='ImagenOferta'


class PalabraClave(models.Model):
    id_palabras_clave = models.AutoField(primary_key=True)
    palabra = models.CharField(max_length=50,unique=True)

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
        db_table= 'ComentarioCalificacion'