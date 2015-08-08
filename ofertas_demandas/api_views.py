
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from ofertas_demandas.models import Oferta
from ofertas_demandas.permissions import SiEsPropietarioOEstaEnAlcance
from ofertas_demandas.serializers import OfertaSerializador

__author__ = 'rbalda'


class OfertaViewSet(ModelViewSet):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializador
    permission_classes = (IsAuthenticated,SiEsPropietarioOEstaEnAlcance)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            Oferta.objects.create(**serializer.validated_data)

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

