from datetime import date, datetime
from ofertas_demandas.models import DiagramaPorter, DiagramaBusinessCanvas, Oferta
from usuarios.serializers import UsuarioSerializador

__author__ = 'rbalda'


from rest_framework.serializers import ModelSerializer


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


class OfertaSerializador(ModelSerializer):
    fk_diagrama_competidores = DiagramaPorterSerializador(required=False,allow_null=True)
    fk_diagrama_canvas = DiagramaBusinessCanvasSerializador(required=False,allow_null=True)

    class Meta:
        model = Oferta
        fields = (
            'id_oferta','codigo','tipo','nombre','publicada','calificacion_total','descripcion','dominio','subdominio',
            'fecha_creacion','fecha_publicacion','tiempo_para_estar_disponible','perfil_beneficiario','perfil_cliente',
            'descripcion_soluciones_existentes','estado_propieada_intelectual','evidencia_traccion','cuadro_tendencias_relevantes',
            'equipo','palabras_clave','comentarios','alcance','fk_diagrama_competidores','fk_diagrama_canvas')

        read_only_fields = ('id_oferta','codigo','fecha_publicacion','fecha_creacion',
                            'calificacion_total','palabras_clave','comentarios','alcance')

    def create(self,validated_data):
        diagrama_competidores = validated_data.pop('fk_diagrama_competidores')
        diagrama_canvas = validated_data.pop('fk_diagrama_canvas')
        diagrama_canvas_exist = False
        competidores_canvas_exist = False

        canvas=None
        porter = None

        for d in diagrama_canvas:
            if not diagrama_canvas[d]==u'':
                diagrama_canvas_exist = True

        for d in diagrama_competidores:
            if not diagrama_competidores[d]=='':
                competidores_canvas_exist = True

        if(competidores_canvas_exist):
           canvas = DiagramaBusinessCanvas.objects.create(**diagrama_canvas)
        if(diagrama_canvas_exist):
            porter = DiagramaPorter.objects.create(**diagrama_competidores)

        oferta = Oferta.objects.create(fk_diagrama_competidores=porter,fk_diagrama_canvas=canvas,codigo=datetime.now().strftime("%I:%M%p on %B %d, %Y"),**validated_data)

        return oferta

