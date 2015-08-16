from django.db import models

# Create your models here.
from usuarios.models import Perfil, Institucion


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
    descripcion_soluciones_existentes = models.TextField(null=True)
    estado_propieada_intelectual = models.TextField(null=True)
    evidencia_traccion = models.TextField(null=True)
    cuadro_tendencias_relevantes = models.TextField(null=True,blank=True)
    fk_diagrama_competidores = models.OneToOneField(DiagramaPorter,related_name='oferta_con_este_diagrama_porter',null=True)
    fk_diagrama_canvas = models.OneToOneField(DiagramaBusinessCanvas,related_name='oferta_con_este_digrama_canvas',null=True)
    equipo = models.ManyToManyField(Perfil,through='MiembroEquipo',through_fields=('fk_oferta_en_que_participa','fk_participante'),related_name='participa_en')
    palabras_clave = models.ManyToManyField('PalabraClave',related_name='ofertas_con_esta_palabra')
    comentarios = models.ManyToManyField(Perfil,through='ComentarioCalificacion',through_fields=('fk_oferta','fk_usuario'),related_name='mis_comentarios')
    alcance = models.ManyToManyField(Institucion,related_name='ofertas_por_institucion')

    class Meta:
        db_table = 'Oferta'
       # unique_together = ('id_oferta','codigo')
       # index_together = ['id_oferta','codigo']


class MiembroEquipo(models.Model):
    id_equipo = models.AutoField(primary_key=True)
    fk_participante = models.ForeignKey(Perfil)
    fk_oferta_en_que_participa = models.ForeignKey(Oferta)
    es_propietario = models.BooleanField(default=False)
    rol_participante = models.TextField(default="Miembro del Equipo de la Oferta")
    activo = models.BooleanField(default=True)
    estado_membresia = models.SmallIntegerField(default=0) #si la membresia esta aceptada rechazada o pendiente

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
        db_table= 'ComentarioCalificacion'


