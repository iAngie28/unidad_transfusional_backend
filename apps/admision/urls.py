from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.admision.views import (
    CitacionDonanteViewSet,
    ConsentimientoInformadoViewSet,
    EspecialidadViewSet,
    MedicoViewSet,
    PacienteViewSet,
    PagoViewSet,
    SolicitudTransfusionViewSet,
)

router = DefaultRouter()
router.register(r"especialidades", EspecialidadViewSet, basename="especialidades")
router.register(r"pacientes", PacienteViewSet, basename="pacientes")
router.register(r"medicos", MedicoViewSet, basename="medicos")
router.register(r"solicitudes-transfusion", SolicitudTransfusionViewSet, basename="solicitudes-transfusion")
router.register(r"consentimientos-informados", ConsentimientoInformadoViewSet, basename="consentimientos-informados")
router.register(r"citaciones-donante", CitacionDonanteViewSet, basename="citaciones-donante")
router.register(r"pagos", PagoViewSet, basename="pagos")

urlpatterns = [
    path("", include(router.urls)),
]
