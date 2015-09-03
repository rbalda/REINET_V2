from ofertas_demandas.api_views import OfertaViewSet
from ofertas_demandas.api_views import MisOfertaViewSet
from ofertas_demandas.api_views import MisOfertaBorradoresViewSet
from ofertas_demandas.api_views import MiembroOfertaViewSet
from ofertas_demandas.api_views import MisOfertasAllViewSet
from ofertas_demandas.api_views import DemandaViewSet
from ofertas_demandas.api_views import MisDemandasViewSet
from ofertas_demandas.api_views import MisDemandasBorradoresViewSet
from ofertas_demandas.api_views import misDemandasAllViewSet

__author__ = 'rbalda'

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'api/ofertas',OfertaViewSet)
router.register(r'api/misOfertas',MisOfertaViewSet)
router.register(r'api/misOfertasBorradores',MisOfertaBorradoresViewSet)
router.register(r'api/miembroOfertas',MiembroOfertaViewSet)
router.register(r'api/misOfertasAll',MisOfertasAllViewSet)

router.register(r'api/demandas',DemandaViewSet)
router.register(r'api/misDemandas',MisDemandasViewSet)
router.register(r'api/misDemandasBorradores', MisDemandasBorradoresViewSet)
router.register(r'api/misDemandasAll',misDemandasAllViewSet)

ofertas_routers = router.urls

