from rest_framework import viewsets

from apps.laboratorio.models import PruebasPretransfHema
from apps.laboratorio.serializers import PruebasPretransfHemaSerializer
from core.views import AuditoriaViewSetMixin, SearchableQuerySetMixin


class PruebasPretransfHemaViewSet(AuditoriaViewSetMixin, SearchableQuerySetMixin, viewsets.ModelViewSet):
    model = PruebasPretransfHema
    serializer_class = PruebasPretransfHemaSerializer
    select_related_fields = ("hemocomponente", "user", "solicitud")
    search_fields = (
        "hemocomponente__nro_bolsa",
        "user__username",
        "solicitud__nro",
        "cruzada_mayor",
        "cruzada_menor",
        "hemolisis",
    )
