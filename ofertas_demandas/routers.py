from ofertas_demandas.api_views import OfertaViewSet
from ofertas_demandas.api_views import MisOfertaViewSet

__author__ = 'rbalda'

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'api/ofertas',OfertaViewSet)
router.register(r'api/misOfertas',MisOfertaViewSet)


ofertas_routers = router.urls

