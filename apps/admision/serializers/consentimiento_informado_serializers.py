from rest_framework import serializers

from apps.admision.models import ConsentimientoInformado, SolicitudTransfusion
from core.serializers import BaseModelSerializer


class ConsentimientoInformadoSerializer(BaseModelSerializer):
    nro_solicitud = serializers.PrimaryKeyRelatedField(
        source="solicitud",
        queryset=SolicitudTransfusion.objects.all(),
    )

    class Meta:
        model = ConsentimientoInformado
        fields = [
            "id",
            "nro_solicitud",
            "fecha",
            "servicio",
            "nombre_familiar",
            "apellido_paterno_familiar",
            "apellido_materno_familiar",
            "telefono",
            "ci",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "created_by"]
