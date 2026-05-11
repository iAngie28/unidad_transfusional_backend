from rest_framework import viewsets

from apps.inventario.models import Descarte
from apps.inventario.serializers import DescarteSerializer
from core.views import AuditoriaViewSetMixin, SearchableQuerySetMixin


class DescarteViewSet(AuditoriaViewSetMixin, SearchableQuerySetMixin, viewsets.ModelViewSet):
    model = Descarte
    serializer_class = DescarteSerializer
    select_related_fields = ("hemocomponente",)
    search_fields = (
        "hemocomponente__nro_bolsa",
        "tipo_accion",
        "motivo",
    )
