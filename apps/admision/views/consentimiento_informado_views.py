from rest_framework import viewsets

from apps.admision.models import ConsentimientoInformado
from apps.admision.serializers import ConsentimientoInformadoSerializer
from core.views import AuditoriaViewSetMixin, SearchableQuerySetMixin


class ConsentimientoInformadoViewSet(AuditoriaViewSetMixin, SearchableQuerySetMixin, viewsets.ModelViewSet):
    model = ConsentimientoInformado
    serializer_class = ConsentimientoInformadoSerializer
    select_related_fields = ("solicitud", "servicio")
    search_fields = (
        "solicitud__nro",
        "servicio__nombre",
        "nombre_familiar",
        "apellido_paterno_familiar",
        "ci",
    )
