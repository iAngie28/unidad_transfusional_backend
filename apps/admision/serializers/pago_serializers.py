from rest_framework import serializers

from apps.admision.models import CitacionDonante, Pago
from apps.laboratorio.models import Transfusion
from core.serializers import BaseModelSerializer


class PagoSerializer(BaseModelSerializer):
    id_citacion = serializers.PrimaryKeyRelatedField(
        source="citacion",
        queryset=CitacionDonante.objects.all(),
        required=False,
        allow_null=True,
    )
    nro_solicitud = serializers.SerializerMethodField()
    paciente_nombre = serializers.SerializerMethodField()
    paciente_ci = serializers.SerializerMethodField()
    id_transfusion = serializers.PrimaryKeyRelatedField(
        source="transfusion",
        queryset=Transfusion.objects.all(),
        required=False,
        allow_null=True,
    )

    def get_nro_solicitud(self, obj):
        if obj.citacion:
            return obj.citacion.solicitud_id
        if obj.transfusion:
            return obj.transfusion.solicitud_id
        return None

    def get_paciente_nombre(self, obj):
        p = None
        if obj.citacion and obj.citacion.solicitud and obj.citacion.solicitud.paciente:
            p = obj.citacion.solicitud.paciente
        elif obj.transfusion and obj.transfusion.solicitud and obj.transfusion.solicitud.paciente:
            p = obj.transfusion.solicitud.paciente
        
        if p:
            materno = f" {p.apellido_materno}" if p.apellido_materno else ""
            return f"{p.apellido_paterno}{materno} {p.nombre}".strip()
        return None

    def get_paciente_ci(self, obj):
        if obj.citacion and obj.citacion.solicitud and obj.citacion.solicitud.paciente:
            return obj.citacion.solicitud.paciente.ci
        if obj.transfusion and obj.transfusion.solicitud and obj.transfusion.solicitud.paciente:
            return obj.transfusion.solicitud.paciente.ci
        return None

    class Meta:
        model = Pago
        fields = [
            "id",
            "estado",
            "es_sus",
            "id_citacion",
            "nro_solicitud",
            "id_transfusion",
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
            "id", "nro_solicitud", "paciente_nombre", "paciente_ci", "created_at", "updated_at", 
            "created_by", "created_by_name", "updated_by", "updated_by_name"
        ]
