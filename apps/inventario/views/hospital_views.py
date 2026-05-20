from rest_framework import viewsets

from apps.inventario.models import Hospital
from apps.inventario.serializers import HospitalSerializer
from core.views import AuditoriaViewSetMixin, SearchableQuerySetMixin


class HospitalViewSet(AuditoriaViewSetMixin, SearchableQuerySetMixin, viewsets.ModelViewSet):
    model = Hospital
    serializer_class = HospitalSerializer
    search_fields = ("nombre", "descripcion")
