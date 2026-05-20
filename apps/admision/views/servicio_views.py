from rest_framework import viewsets

from apps.admision.models import Servicio
from apps.admision.serializers import ServicioSerializer
from core.views import AuditoriaViewSetMixin, SearchableQuerySetMixin


class ServicioViewSet(AuditoriaViewSetMixin, SearchableQuerySetMixin, viewsets.ModelViewSet):
    model = Servicio
    serializer_class = ServicioSerializer
    search_fields = ("nombre", "descripcion")
