from .api_views import IncubacionViewSet
from rest_framework.routers import DefaultRouter

__author__ = 'faustomora'

router = DefaultRouter()

router.register(r'api/incubacion',IncubacionViewSet)

incubacion_routers = router.urls