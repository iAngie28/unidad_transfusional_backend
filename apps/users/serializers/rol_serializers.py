from django.contrib.auth.models import Permission
from rest_framework import serializers

from apps.users.models import Rol
from core.serializers import BaseModelSerializer


class PermisoSerializer(serializers.ModelSerializer):
    modulo = serializers.CharField(source="content_type.name", read_only=True)
    app = serializers.CharField(source="content_type.app_label", read_only=True)

    class Meta:
        model = Permission
        fields = ["id", "codename", "name", "modulo", "app"]


class RolSerializer(BaseModelSerializer):
    permisos = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Permission.objects.all(),
        required=False,
    )
    permisos_detalle = PermisoSerializer(
        source="permisos",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Rol
        fields = ["id", "nombre", "descripcion", "permisos", "permisos_detalle"]
