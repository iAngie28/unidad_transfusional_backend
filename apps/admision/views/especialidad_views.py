from rest_framework import viewsets

from apps.admision.models import Especialidad
from apps.admision.serializers import EspecialidadSerializer
from core.views import AuditoriaViewSetMixin, SearchableQuerySetMixin


class EspecialidadViewSet(AuditoriaViewSetMixin, SearchableQuerySetMixin, viewsets.ModelViewSet):
    model = Especialidad
    serializer_class = EspecialidadSerializer
    search_fields = ("nombre", "descripcion")
