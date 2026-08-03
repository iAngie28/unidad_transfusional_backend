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
    paciente_nombre = serializers.SerializerMethodField()
    paciente_ci = serializers.SerializerMethodField()

    def get_paciente_nombre(self, obj):
        if obj.solicitud and obj.solicitud.paciente:
            p = obj.solicitud.paciente
            materno = f" {p.apellido_materno}" if p.apellido_materno else ""
            return f"{p.apellido_paterno}{materno} {p.nombre}".strip()
        return None

    def get_paciente_ci(self, obj):
        if obj.solicitud and obj.solicitud.paciente:
            return obj.solicitud.paciente.ci
        return None

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
            "paciente_nombre",
            "paciente_ci",
            "created_at",
            "updated_at",
            "created_by",
            "created_by_name",
            "updated_by",
            "updated_by_name",
        ]
        read_only_fields = [
            "id", "servicio_nombre", "paciente_nombre", "paciente_ci", "created_at", "updated_at", 
            "created_by", "created_by_name", "updated_by", "updated_by_name"
        ]
        service_class = ConsentimientoInformadoValidationService
