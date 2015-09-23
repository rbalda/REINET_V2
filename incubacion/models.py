import datetime
from django.db import models

# Create your models here.
from usuarios.models import Perfil, Institucion
from ofertas_demandas.models import Oferta,DiagramaPorter,DiagramaBusinessCanvas,MiembroEquipo,PalabraClave

def definir_ruta_imagen_incubada(self, filename):
    hoy = datetime.datetime.now().strftime("%Y%m%d%H%M")
    nombre_archivo_hoy = "%s_%s" % (hoy, filename)
    return "incubadas/%s/galeria/%s" % (self.fk_incubada.codigo, nombre_archivo_hoy)


class Incubacion(models.Model):
	id_incubacion=models.AutoField(primary_key=True)
	nombre=models.CharField(max_length=300)
	fecha_inicio = models.DateTimeField()
	descripcion = models.TextField()
	perfil_oferta = models.TextField()
	condiciones = models.TextField()
	tipos_oferta = models.PositiveSmallIntegerField()
	otros = models.TextField(null=True,blank=True)
	estado_incubacion = models.PositiveSmallIntegerField(default=0)#activa=0,terminada=1,desactivada=2
	fk_perfil = models.ForeignKey(Perfil)
	class Meta:
		db_table = 'Incubacion'

class Consultor(models.Model):
	id_consultor = models.AutoField(primary_key=True)
	fk_usuario_consultor = models.ForeignKey(Perfil)
	fecha_creacion = models.DateField(default=datetime.date.today)
	class Meta:
		db_table = 'Consultor'

class Incubada(models.Model):
    id_incubada = models.AutoField(primary_key=True)
    codigo = models.SlugField(unique=True) #CAMPO QUE SE DEBE MOSTRAR EN EL URL
    tipo = models.PositiveSmallIntegerField()
    nombre = models.CharField(max_length=300)
    descripcion = models.TextField()
    dominio = models.TextField()
    subdominio = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_publicacion = models.DateTimeField('Publicada',null=True,blank=True)
    tiempo_para_estar_disponible = models.CharField(max_length=25)
    perfil_beneficiario = models.TextField(null=True,blank=True)
    perfil_cliente = models.TextField(null=True,blank=True)
    descripcion_soluciones_existentes = models.TextField(null=True,blank=True)
    estado_propiedad_intelectual = models.TextField(null=True,blank=True)
    evidencia_traccion = models.TextField(null=True,blank=True)
    cuadro_tendencias_relevantes = models.TextField(null=True,blank=True)
    fk_diagrama_competidores = models.OneToOneField(DiagramaPorter,related_name='incubada_con_este_diagrama_porter',null=True)
    fk_diagrama_canvas = models.OneToOneField(DiagramaBusinessCanvas,related_name='incubada_con_este_digrama_canvas',null=True)
    #equipo = models.ManyToManyField(Perfil,through='MiembroEquipo',through_fields=('fk_oferta_en_que_participa','fk_participante'),related_name='participa_en')
    equipo = models.ForeignKey(MiembroEquipo)
    palabras_clave = models.ManyToManyField(PalabraClave,related_name='incubada_con_esta_palabra')
    #comentarios = models.ManyToManyField(Perfil,through='ComentarioCalificacion',through_fields=('fk_oferta','fk_usuario'),related_name='mis_comentarios')
    #alcance = models.ManyToManyField(Institucion,related_name='ofertas_por_institucion')
    fk_oferta=models.ForeignKey(Oferta,default=30)
    fk_incubacion = models.ForeignKey(Incubacion)
    consultores=models.ManyToManyField(Consultor,through='IncubadaConsultor',through_fields=('fk_incubada','fk_consultor'),related_name='consultores')
    class Meta:
        db_table = 'Incubada'


class ImagenIncubada(models.Model):
    id_imagen = models.AutoField(primary_key=True)
    imagen = models.ImageField(upload_to=definir_ruta_imagen_incubada)
    descripcion = models.TextField()
    fk_incubada = models.ForeignKey(Incubada,related_name='galeriaIncubada')
    class Meta:
        db_table='ImagenIncubada'

class IncubadaConsultor(models.Model):
	id_incubadaConsultor = models.AutoField(primary_key=True)
	fk_consultor = models.ForeignKey(Consultor)
	fk_incubada = models.ForeignKey(Incubada)
	fecha_creacion = models.DateField(default=datetime.date.today)
	class Meta:
		db_table = 'IncubadaConsultor'

class Milestone(models.Model):
	id_milestone = models.AutoField(primary_key=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_maxima_Retroalimentacion = models.DateTimeField()
	fecha_maxima = models.DateTimeField()
	requerimientos = models.TextField()
	importancia = models.TextField()
	otros = models.TextField(null=True,blank=True)
	fk_incubada = models.ForeignKey(Incubada)
	retroalimentaciones=models.ManyToManyField(Consultor,through='Retroalimentacion',through_fields=('fk_milestone','fk_consultor'),related_name='retroalimentaciones')
	class Meta:
		db_table = 'Milestone'

class Retroalimentacion(models.Model):
	id_retroalimentacion = models.AutoField(primary_key=True)
	num_tab=models.PositiveSmallIntegerField()
	contenido = models.TextField()
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fk_milestone = models.ForeignKey(Milestone)
	fk_consultor = models.ForeignKey(Consultor)
	class Meta:
		db_table = 'Retroalimentacion'

class Convocatoria(models.Model):
	id_convocatoria_ofertas=models.AutoField(primary_key=True)
	fecha_creacion= models.DateTimeField(auto_now_add=True)
	fecha_maxima= models.DateTimeField()
	solicitudes=models.ManyToManyField(Oferta,through='SolicitudOfertasConvocatoria',through_fields=('fk_convocatoria','fk_oferta'),related_name='solicitudes_Ofertas')
	otros = models.TextField(null=True,blank=True)
	fk_incubacion = models.ForeignKey(Incubacion)
	class Meta:
		db_table = 'Convocatoria'

class SolicitudOfertasConvocatoria(models.Model):
	id_solicitud_ofertas_convocatoria=models.AutoField(primary_key=True)
	estado_solicitud=models.PositiveSmallIntegerField() #Pendiente=0,Aprobada=1,Rechazada=2
	fk_convocatoria=models.ForeignKey(Convocatoria)
	fk_oferta=models.ForeignKey(Oferta)
	fecha_creacion= models.DateTimeField(auto_now_add=True)
	class Meta:
		db_table='SolicitudOfertasConvocatoria'
