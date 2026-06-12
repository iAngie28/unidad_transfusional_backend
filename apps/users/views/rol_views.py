from django.contrib.auth.models import Permission
from rest_framework import mixins, viewsets

from apps.users.models import Rol
from apps.users.serializers.rol_serializers import PermisoSerializer, RolSerializer
from core.views import AuthenticatedViewSetMixin, SearchableQuerySetMixin


class RolViewSet(AuthenticatedViewSetMixin, SearchableQuerySetMixin, viewsets.ModelViewSet):
    model = Rol
    serializer_class = RolSerializer
    prefetch_related_fields = ("permisos",)
    search_fields = ("nombre", "descripcion")

class PermissionViewSet(AuthenticatedViewSetMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Permission.objects.select_related('content_type').all()
    serializer_class = PermisoSerializer
    pagination_class = None # Listar todos sin paginar
