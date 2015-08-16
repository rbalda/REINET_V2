from ofertas_demandas.api_views import OfertaViewSet
from ofertas_demandas.api_views import MisOfertaViewSet
from ofertas_demandas.api_views import MisOfertaBorradoresViewSet
from ofertas_demandas.api_views import MiembroOfertaViewSet

__author__ = 'rbalda'

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'api/ofertas',OfertaViewSet)
router.register(r'api/misOfertas',MisOfertaViewSet)
router.register(r'api/misOfertasBorradores',MisOfertaBorradoresViewSet)
router.register(r'api/miembroOfertas',MiembroOfertaViewSet)


ofertas_routers = router.urls

