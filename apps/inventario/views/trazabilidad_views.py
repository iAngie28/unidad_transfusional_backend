from rest_framework import viewsets

from apps.inventario.models import Trazabilidad
from apps.inventario.serializers import TrazabilidadSerializer
from core.views import AuditoriaViewSetMixin, SearchableQuerySetMixin


class TrazabilidadViewSet(AuditoriaViewSetMixin, SearchableQuerySetMixin, viewsets.ModelViewSet):
    model = Trazabilidad
    serializer_class = TrazabilidadSerializer
    select_related_fields = ("hemocomponente", "encargado")
    search_fields = (
        "hemocomponente__nro_bolsa",
        "evento",
        "encargado__username",
        "encargado__first_name",
        "encargado__last_name",
    )
