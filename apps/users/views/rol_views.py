from rest_framework import viewsets

from apps.users.models import Rol
from apps.users.serializers.rol_serializers import RolSerializer
from core.views import AuthenticatedViewSetMixin, SearchableQuerySetMixin


class RolViewSet(AuthenticatedViewSetMixin, SearchableQuerySetMixin, viewsets.ModelViewSet):
    model = Rol
    serializer_class = RolSerializer
    prefetch_related_fields = ("permisos",)
    search_fields = ("nombre", "descripcion")
