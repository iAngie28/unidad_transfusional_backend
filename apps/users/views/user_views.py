from rest_framework import viewsets

from apps.users.models import User
from apps.users.serializers.user_serializers import UserSerializer
from core.views import AuthenticatedViewSetMixin, SearchableQuerySetMixin


class UserViewSet(AuthenticatedViewSetMixin, SearchableQuerySetMixin, viewsets.ModelViewSet):
    model = User
    serializer_class = UserSerializer
    select_related_fields = ("rol",)
    ordering_fields = ("id",)
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "apellido_materno",
        "telefono",
        "rol__nombre",
    )
