from django.contrib.auth.models import Permission
from rest_framework import serializers

from apps.users.models import Rol
from core.serializers import BaseModelSerializer


class PermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "codename", "name", "content_type"]


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
