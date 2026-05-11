from rest_framework import viewsets

from apps.inventario.models import Hemocomponente
from apps.inventario.serializers import HemocomponenteSerializer
from core.views import AuditoriaViewSetMixin, SearchableQuerySetMixin


class HemocomponenteViewSet(AuditoriaViewSetMixin, SearchableQuerySetMixin, viewsets.ModelViewSet):
    model = Hemocomponente
    serializer_class = HemocomponenteSerializer
    search_fields = (
        "nro_bolsa",
        "nro_tubuladura",
        "tipo",
        "grupo_sanguineo",
        "estado",
    )
