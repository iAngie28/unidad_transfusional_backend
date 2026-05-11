from rest_framework import viewsets

from apps.admision.models import Medico
from apps.admision.serializers import MedicoSerializer
from core.views import AuditoriaViewSetMixin, SearchableQuerySetMixin


class MedicoViewSet(AuditoriaViewSetMixin, SearchableQuerySetMixin, viewsets.ModelViewSet):
    model = Medico
    serializer_class = MedicoSerializer
    select_related_fields = ("especialidad",)
    search_fields = (
        "nombre",
        "apellido_paterno",
        "apellido_materno",
        "especialidad__nombre",
        "matricula_profesional",
    )
