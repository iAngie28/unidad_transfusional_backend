from rest_framework import viewsets

from apps.admision.models import Pago
from apps.admision.serializers import PagoSerializer
from core.views import AuditoriaViewSetMixin, SearchableQuerySetMixin


class PagoViewSet(AuditoriaViewSetMixin, SearchableQuerySetMixin, viewsets.ModelViewSet):
    model = Pago
    serializer_class = PagoSerializer
    select_related_fields = ("citacion", "citacion__solicitud", "transfusion", "transfusion__paciente")
    search_fields = (
        "estado",
        "citacion__codigo_donante",
        "citacion__solicitud__nro",
        "transfusion__paciente__ci",
    )
