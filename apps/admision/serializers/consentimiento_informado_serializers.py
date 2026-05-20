from rest_framework import serializers

from apps.admision.models import ConsentimientoInformado, Servicio, SolicitudTransfusion
from apps.admision.services import ConsentimientoInformadoValidationService
from core.serializers import BaseModelSerializer


class ConsentimientoInformadoSerializer(BaseModelSerializer):
    nro_solicitud = serializers.PrimaryKeyRelatedField(
        source="solicitud",
        queryset=SolicitudTransfusion.objects.all(),
    )
    id_servicio = serializers.PrimaryKeyRelatedField(
        source="servicio",
        queryset=Servicio.objects.all(),
    )
    servicio_nombre = serializers.CharField(source="servicio.nombre", read_only=True)

    class Meta:
        model = ConsentimientoInformado
        fields = [
            "id",
            "nro_solicitud",
            "fecha",
            "id_servicio",
            "servicio_nombre",
            "nombre_familiar",
            "apellido_paterno_familiar",
            "apellido_materno_familiar",
            "telefono",
            "ci",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = ["id", "servicio_nombre", "created_at", "updated_at", "created_by"]
        service_class = ConsentimientoInformadoValidationService
