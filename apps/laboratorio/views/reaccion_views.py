from rest_framework import viewsets

from apps.laboratorio.models import Reaccion
from apps.laboratorio.serializers import ReaccionSerializer
from core.views import AuditoriaViewSetMixin, SearchableQuerySetMixin


class ReaccionViewSet(AuditoriaViewSetMixin, SearchableQuerySetMixin, viewsets.ModelViewSet):
    model = Reaccion
    serializer_class = ReaccionSerializer
    select_related_fields = ("transfusion", "transfusion__paciente")
    search_fields = (
        "transfusion__paciente__ci",
        "descripcion",
    )
