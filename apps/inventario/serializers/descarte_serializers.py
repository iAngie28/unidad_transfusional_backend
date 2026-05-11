from rest_framework import serializers

from apps.inventario.models import Descarte, Hemocomponente
from core.serializers import BaseModelSerializer


class DescarteSerializer(BaseModelSerializer):
    nro_bolsa = serializers.PrimaryKeyRelatedField(
        source="hemocomponente",
        queryset=Hemocomponente.objects.all(),
    )

    class Meta:
        model = Descarte
        fields = [
            "id",
            "nro_bolsa",
            "tipo_accion",
            "motivo",
            "fecha_hora",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "created_by"]
