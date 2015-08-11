from ofertas_demandas.api_views import OfertaViewSet

__author__ = 'rbalda'

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'api/ofertas',OfertaViewSet)


ofertas_routers = router.urls

