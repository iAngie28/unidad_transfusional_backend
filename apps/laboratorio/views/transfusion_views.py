from rest_framework import viewsets

from apps.laboratorio.models import Transfusion
from apps.laboratorio.serializers import TransfusionSerializer
from core.views import AuditoriaViewSetMixin, SearchableQuerySetMixin


class TransfusionViewSet(AuditoriaViewSetMixin, SearchableQuerySetMixin, viewsets.ModelViewSet):
    model = Transfusion
    serializer_class = TransfusionSerializer
    select_related_fields = ("hemocomponente", "paciente", "user")
    search_fields = (
        "hemocomponente__nro_bolsa",
        "paciente__ci",
        "paciente__nombre",
        "paciente__apellido_paterno",
        "user__username",
        "servicio",
        "diagnostico",
        "grupo_cabecera_h",
    )
