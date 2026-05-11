from rest_framework import viewsets

from apps.laboratorio.models import PruebaPretransfusionalPAC
from apps.laboratorio.serializers import PruebaPretransfusionalPACSerializer
from core.views import AuditoriaViewSetMixin, SearchableQuerySetMixin


class PruebaPretransfusionalPACViewSet(AuditoriaViewSetMixin, SearchableQuerySetMixin, viewsets.ModelViewSet):
    model = PruebaPretransfusionalPAC
    serializer_class = PruebaPretransfusionalPACSerializer
    select_related_fields = ("paciente", "user", "solicitud")
    search_fields = (
        "paciente__ci",
        "paciente__nombre",
        "paciente__apellido_paterno",
        "user__username",
        "solicitud__nro",
        "resultado",
    )
