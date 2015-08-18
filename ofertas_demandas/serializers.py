# -*- encoding: utf-8 -*-

from datetime import date, datetime
from ofertas_demandas.models import DiagramaPorter, DiagramaBusinessCanvas, Oferta, MiembroEquipo, PalabraClave
from usuarios.models import Perfil
from rest_framework import serializers
import json

__author__ = 'rbalda'


from rest_framework.serializers import ModelSerializer

def crear_codigo(nombre_oferta):
    nombre_oferta.replace(' ','-')
    return '%s-%s'%(nombre_oferta,datetime.now().strftime("%Y-%m-%d-%H-%M"))


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


class PalabrasClaveSerializador(ModelSerializer):
    class Meta:
        model = PalabraClave
        fields = ('palabra')
        read_only_fields = ('id_palabras_clave')


class OfertaSerializador(ModelSerializer):
    fk_diagrama_competidores = DiagramaPorterSerializador(required=False,allow_null=True)
    fk_diagrama_canvas = DiagramaBusinessCanvasSerializador(required=False,allow_null=True)
    dueno = serializers.SerializerMethodField('getdueno',read_only=True)
    duenoUsername = serializers.SerializerMethodField('getDuenoUsername',read_only=True)

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
            'equipo','tags','comentarios','alcance','fk_diagrama_competidores','fk_diagrama_canvas','palabras_clave', 'dueno', 'duenoUsername')

        read_only_fields = ('id_oferta','codigo','fecha_publicacion','fecha_creacion',
                            'calificacion_total','comentarios','palabras_clave','alcance')


    def getdueno(self,obj):
        equipoDueno = MiembroEquipo.objects.all().filter(es_propietario=1, fk_oferta_en_que_participa=obj.id_oferta).first()
        return equipoDueno.fk_participante.first_name + ' ' + equipoDueno.fk_participante.last_name

    def getDuenoUsername(self,obj):
        equipoDueno = MiembroEquipo.objects.all().filter(es_propietario=1, fk_oferta_en_que_participa=obj.id_oferta).first()
        return equipoDueno.fk_participante.username

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

