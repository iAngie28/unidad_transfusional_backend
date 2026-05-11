from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.laboratorio.views import (
    PruebaPretransfusionalPACViewSet,
    PruebasPretransfHemaViewSet,
    ReaccionViewSet,
    TransfusionViewSet,
)

router = DefaultRouter()
router.register(r"pruebas-pac", PruebaPretransfusionalPACViewSet, basename="pruebas-pac")
router.register(r"pruebas-hema", PruebasPretransfHemaViewSet, basename="pruebas-hema")
router.register(r"transfusiones", TransfusionViewSet, basename="transfusiones")
router.register(r"reacciones", ReaccionViewSet, basename="reacciones")

urlpatterns = [
    path("", include(router.urls)),
]
