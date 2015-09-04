# -*- encoding: utf-8 -*-

from datetime import date, datetime
from django.contrib.admin.utils import model_format_dict
from ofertas_demandas.models import DiagramaPorter, DiagramaBusinessCanvas, Oferta, ComentarioCalificacion, MiembroEquipo, PalabraClave, \
    ImagenOferta, Demanda, ImagenDemanda, ComentarioDemanda
from usuarios.models import Perfil
from rest_framework import serializers
import json

__author__ = 'rbalda'


from rest_framework.serializers import ModelSerializer

def crear_codigo(nombre_oferta):
    nombre_oferta = " ".join(nombre_oferta.split())
    nombre = nombre_oferta.replace(" ","-")
    return '%s-%s'%(nombre,datetime.now().strftime("%Y-%m-%d-%H-%M"))


class ImagenOfertaSerializer(ModelSerializer):
    imagen = serializers.ImageField()
    class Meta:
        model=ImagenOferta
        fields=('imagen','descripcion')

class ImagenDemandaSerializer(ModelSerializer):
    imagen = serializers.ImageField()
    class Meta:
        model=ImagenDemanda
        fields=('imagen','descripcion')

class DiagramaPorterSerializador(ModelSerializer):
    class Meta:
        model = DiagramaPorter
        fields = ('id_diagrama_porter','competidores','sustitutos','consumidores','proveedores','nuevosMiembros')
        read_only_fields = ('id_diagrama_porter',)


class DiagramaBusinessCanvasSerializador(ModelSerializer):
    class Meta:
        model = DiagramaBusinessCanvas
        fields = ('id_diagrama_business_canvas','asociaciones_clave','actividades_clave','recursos_clave','propuesta_valor',
                  'relacion_clientes','canales_distribucion','segmento_mercado','estructura_costos','fuente_ingresos')
        read_only_fields = ('id_diagrama_canvas',)


class PalabraClaveSerializador(ModelSerializer):
    class Meta:
        model = PalabraClave
        fields = ('palabra',)


class OfertaSerializador(ModelSerializer):
    fk_diagrama_competidores = DiagramaPorterSerializador(required=False,allow_null=True)
    fk_diagrama_canvas = DiagramaBusinessCanvasSerializador(required=False,allow_null=True)
    dueno = serializers.SerializerMethodField('getdueno',read_only=True)
    duenoUsername = serializers.SerializerMethodField('getDuenoUsername',read_only=True)
    numComentarios = serializers.SerializerMethodField('getNumeroComentarios',read_only=True)
    palabras_clave = PalabraClaveSerializador(required=False,read_only=True,many=True)
    galeria = ImagenOfertaSerializer(many=True,required=False)
    tags = serializers.ListField(
            child=serializers.CharField(),
            required=False,allow_null=True
    )


    class Meta:
        model = Oferta
        fields = (
            'id_oferta','codigo','tipo','nombre','publicada','calificacion_total','descripcion','dominio','subdominio',
            'fecha_creacion','fecha_publicacion','tiempo_para_estar_disponible','perfil_beneficiario','perfil_cliente',
            'descripcion_soluciones_existentes','estado_propieada_intelectual','evidencia_traccion','cuadro_tendencias_relevantes',
            'equipo','tags','comentarios','alcance','fk_diagrama_competidores','fk_diagrama_canvas','palabras_clave', 'dueno',
            'duenoUsername','galeria', 'numComentarios')

        read_only_fields = ('id_oferta','codigo','fecha_publicacion','fecha_creacion',
                            'calificacion_total','comentarios','palabras_clave','alcance','galeria')


    def getdueno(self,obj):
        equipoDueno = MiembroEquipo.objects.all().filter(es_propietario=1, fk_oferta_en_que_participa=obj.id_oferta).first()
        return equipoDueno.fk_participante.first_name + ' ' + equipoDueno.fk_participante.last_name

    def getDuenoUsername(self,obj):
        equipoDueno = MiembroEquipo.objects.all().filter(es_propietario=1, fk_oferta_en_que_participa=obj.id_oferta).first()
        return equipoDueno.fk_participante.username

    def getNumeroComentarios(self,obj):
        numComentarios = len(ComentarioCalificacion.objects.all().filter(fk_oferta_id = obj.id_oferta, estado_comentario = 1))
        return numComentarios

    def create(self,validated_data):
        diagrama_competidores = validated_data.pop('fk_diagrama_competidores',None)
        diagrama_canvas = validated_data.pop('fk_diagrama_canvas',None)
        tags = validated_data.pop('tags',None)
        diagrama_canvas_exist = False
        competidores_canvas_exist = False

        canvas=None
        porter = None

        if diagrama_canvas:
            for d in diagrama_canvas:
                if not diagrama_canvas[d]==u'':
                    diagrama_canvas_exist = True

        if diagrama_competidores:       
            for d in diagrama_competidores:
                if not diagrama_competidores[d]=='':
                    competidores_canvas_exist = True


        if(competidores_canvas_exist):
           canvas = DiagramaBusinessCanvas.objects.create(**diagrama_canvas)
        if(diagrama_canvas_exist):
            porter = DiagramaPorter.objects.create(**diagrama_competidores)

        nombre = validated_data['nombre']
        oferta = Oferta.objects.create(fk_diagrama_competidores=porter,fk_diagrama_canvas=canvas,codigo=crear_codigo(nombre),**validated_data)
        MiembroEquipo.objects.create(fk_participante=Perfil.objects.get(id=self.context['request'].user.id),fk_oferta_en_que_participa=oferta,
                                     es_propietario=True,rol_participante='dueño de la oferta',estado_membresia=1,activo = True)

        if tags:
            for d in tags:
                aux = d.encode('utf-8','ignore')
                palabra = aux.replace("{u'text': u'", "")
                palabra = palabra.replace("'}","")
                palabra = palabra.replace(" ",'')
                palabra = palabra.lower()

                try:
                    tag = PalabraClave.objects.get(palabra=palabra)
                    oferta.palabras_clave.add(tag)
                except PalabraClave.DoesNotExist:
                    palabra_clave = PalabraClave.objects.create(palabra=palabra)
                    oferta.palabras_clave.add(palabra_clave)
                except Exception as e:
                    print type(e)
                    print e

        return oferta



class DemandaSerializador(ModelSerializer):
    dueno = serializers.SerializerMethodField('getdueno',read_only=True)
    duenoUsername = serializers.SerializerMethodField('getDuenoUsername',read_only=True)
    palabras_clave = PalabraClaveSerializador(required=False,read_only=True,many=True)
    numComentarios = serializers.SerializerMethodField('getNumeroComentarios',read_only=True)
    galeria = ImagenDemandaSerializer(many=True,required=False)
    tags = serializers.ListField(
            child=serializers.CharField(),
            required=False,allow_null=True
    )

    class Meta:
        model = Demanda
        fields = (
            'id_demanda','codigo','estado','nombre','publicada','descripcion','dominio','subdominio',
            'fecha_creacion','fecha_publicacion','tiempo_para_estar_disponible','perfil_beneficiario','perfil_cliente',
            'alternativas_soluciones_existentes','lugar_donde_necesita','importancia_resolver_necesidad','tags','alcance','palabras_clave','comentarios', 'dueno',
            'duenoUsername','galeria', 'numComentarios')

        read_only_fields = ('id_oferta','codigo','estado','fecha_publicacion','fecha_creacion',
                            'palabras_clave','alcance','comentarios','galeria')

    def getdueno(self,obj):
        perfil = Perfil.objects.all().filter(id_perfil = obj.fk_perfil_id).first()
        return perfil.first_name + ' ' + perfil.last_name

    def getDuenoUsername(self,obj):
        perfil = Perfil.objects.all().filter(id_perfil = obj.fk_perfil_id).first()
        return perfil.username

    def create(self,validated_data):
        tags = validated_data.pop('tags',None)

    def getNumeroComentarios(self,obj):
        numComentarios = len(ComentarioDemanda.objects.all().filter(fk_demanda_id = obj.id_demanda, estado_comentario = 1))
        return numComentarios

        nombre = validated_data['nombre']
        demanda = Demanda.objects.create(codigo=crear_codigo(nombre),estado=1,fk_perfil=Perfil.objects.get(id=self.context['request'].user.id),**validated_data)
        
        if tags:
            for d in tags:
                aux = d.encode('utf-8','ignore')
                palabra = aux.replace("{u'text': u'", "")
                palabra = palabra.replace("'}","")
                palabra = palabra.replace(" ",'')
                palabra = palabra.lower()

                try:
                    tag = PalabraClave.objects.get(palabra=palabra)
                    demanda.palabras_clave.add(tag)
                except PalabraClave.DoesNotExist:
                    palabra_clave = PalabraClave.objects.create(palabra=palabra)
                    demanda.palabras_clave.add(palabra_clave)
                except Exception as e:
                    print type(e)
                    print e

        return demanda