from rest_framework import serializers

from apps.inventario.models import Descarte, Hemocomponente, Hospital
from apps.inventario.services import DescarteValidationService
from core.serializers import BaseModelSerializer


class DescarteSerializer(BaseModelSerializer):
    nro_bolsa = serializers.PrimaryKeyRelatedField(
        source="hemocomponente",
        queryset=Hemocomponente.objects.all(),
    )
    hospital_nombre = serializers.CharField(source="hospital.nombre", read_only=True)
    hospital = serializers.PrimaryKeyRelatedField(
        queryset=Hospital.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Descarte
        service_class = DescarteValidationService
        fields = [
            "id",
            "nro_bolsa",
            "tipo_accion",
            "motivo",
            "hospital",
            "hospital_nombre",
            "fecha_hora",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "created_by"]
        extra_kwargs = {
            "motivo": {"required": False, "allow_null": True, "allow_blank": True},
        }
