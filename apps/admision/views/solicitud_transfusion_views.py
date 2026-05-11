from rest_framework import viewsets

from apps.admision.models import SolicitudTransfusion
from apps.admision.serializers import SolicitudTransfusionSerializer
from core.views import AuditoriaViewSetMixin, SearchableQuerySetMixin


class SolicitudTransfusionViewSet(AuditoriaViewSetMixin, SearchableQuerySetMixin, viewsets.ModelViewSet):
    model = SolicitudTransfusion
    serializer_class = SolicitudTransfusionSerializer
    select_related_fields = ("user", "paciente", "medico")
    search_fields = (
        "nro",
        "paciente__ci",
        "paciente__nombre",
        "paciente__apellido_paterno",
        "medico__nombre",
        "medico__apellido_paterno",
        "diagnostico",
        "hemocomponente",
        "tipo_urgencia",
    )
