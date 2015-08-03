from ofertas_demandas.models import DiagramaPorter, DiagramaBusinessCanvas, Oferta

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
    fk_diagrama_competidores = DiagramaPorterSerializador()
    fk_diagrama_canvas = DiagramaBusinessCanvasSerializador()
    class Meta:
        model = Oferta
        fields = (
            'id_oferta','codigo','tipo','nombre','publicada','calificacion_total','descripcion','dominio','subdominio',
            'fecha_creacion','fecha_publicacion','tiempo_para_estar_disponible','perfil_beneficiario','perfil_cliente',
            'descripcion_soluciones_existentes','estado_propieada_intelectual','evidencia_traccion','cuadro_tendencias_relevantes',
            'equipo','palabras_clave','comentarios','alcance','fk_diagrama_competidores','fk_diagrama_canvas')

        read_only_fields = ('id_oferta','codigo','fecha_publicacion','fecha_creacion')




