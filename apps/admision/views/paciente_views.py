from rest_framework import viewsets

from apps.admision.models import Paciente
from apps.admision.serializers import PacienteSerializer
from core.views import AuditoriaViewSetMixin, SearchableQuerySetMixin


class PacienteViewSet(AuditoriaViewSetMixin, SearchableQuerySetMixin, viewsets.ModelViewSet):
    model = Paciente
    serializer_class = PacienteSerializer
    search_fields = (
        "ci",
        "nombre",
        "apellido_paterno",
        "apellido_materno",
        "historia_clinica",
        "grupo_sanguineo",
    )
