from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.inventario.models import Hemocomponente, Trazabilidad
from core.serializers import BaseModelSerializer

User = get_user_model()


class TrazabilidadSerializer(BaseModelSerializer):
    nro_bolsa = serializers.PrimaryKeyRelatedField(
        source="hemocomponente",
        queryset=Hemocomponente.objects.all(),
    )
    encargado = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    encargado_username = serializers.CharField(source="encargado.username", read_only=True)

    class Meta:
        model = Trazabilidad
        fields = [
            "id",
            "nro_bolsa",
            "evento",
            "encargado",
            "encargado_username",
            "fecha_hora",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = ["id", "encargado_username", "created_at", "updated_at", "created_by"]
