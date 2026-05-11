from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.inventario.views import (
    DescarteViewSet,
    HemocomponenteViewSet,
    TrazabilidadViewSet,
)

router = DefaultRouter()
router.register(r"hemocomponentes", HemocomponenteViewSet, basename="hemocomponentes")
router.register(r"trazabilidades", TrazabilidadViewSet, basename="trazabilidades")
router.register(r"descartes", DescarteViewSet, basename="descartes")

urlpatterns = [
    path("", include(router.urls)),
]
