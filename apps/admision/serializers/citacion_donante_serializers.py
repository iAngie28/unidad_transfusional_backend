from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.admision.models import CitacionDonante, CodigoDonante, Servicio, SolicitudTransfusion
from apps.admision.services import CitacionDonanteValidationService
from core.serializers import BaseModelSerializer

User = get_user_model()


class CodigoDonanteSerializer(BaseModelSerializer):
    class Meta:
        model = CodigoDonante
        fields = ["id", "codigo", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class CitacionDonanteSerializer(BaseModelSerializer):
    nro_solicitud = serializers.PrimaryKeyRelatedField(
        source="solicitud",
        queryset=SolicitudTransfusion.objects.all(),
    )
    id_user = serializers.PrimaryKeyRelatedField(source="user", queryset=User.objects.all())
    id_servicio = serializers.PrimaryKeyRelatedField(source="servicio", queryset=Servicio.objects.all())
    user_username = serializers.CharField(source="user.username", read_only=True)
    servicio_nombre = serializers.CharField(source="servicio.nombre", read_only=True)
    paciente_nombre = serializers.SerializerMethodField()
    paciente_ci = serializers.SerializerMethodField()
    codigos_donante = CodigoDonanteSerializer(many=True)
    bolsas_a_favor = serializers.SerializerMethodField()

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

    def get_bolsas_a_favor(self, obj):
        return obj.codigos_donante.count() - obj.cantidad

    def create(self, validated_data):
        codigos_data = validated_data.pop('codigos_donante', [])
        citacion = super().create(validated_data)
        for codigo_data in codigos_data:
            CodigoDonante.objects.create(
                citacion=citacion, 
                created_by=citacion.created_by,
                **codigo_data
            )
        return citacion

    def update(self, instance, validated_data):
        codigos_data = validated_data.pop('codigos_donante', None)
        instance = super().update(instance, validated_data)
        
        if codigos_data is not None:
            # Delete old codes and recreate
            instance.codigos_donante.all().delete()
            for codigo_data in codigos_data:
                CodigoDonante.objects.create(
                    citacion=instance, 
                    created_by=instance.updated_by or instance.created_by,
                    **codigo_data
                )
        return instance

    class Meta:
        model = CitacionDonante
        fields = [
            "id",
            "nro_solicitud",
            "id_user",
            "user_username",
            "fecha",
            "id_servicio",
            "servicio_nombre",
            "sala_cama",
            "cantidad",
            "codigos_donante",
            "bolsas_a_favor",
            "hora",
            "grupo_factor",
            "tipo",
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
            "id", "user_username", "servicio_nombre", "paciente_nombre", "paciente_ci",
            "bolsas_a_favor", "created_at", "updated_at", "created_by", 
            "created_by_name", "updated_by", "updated_by_name"
        ]
        service_class = CitacionDonanteValidationService
