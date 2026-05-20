from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.admision.models import Medico, Paciente, SolicitudTransfusion
from apps.admision.services import SolicitudTransfusionValidationService
from core.serializers import BaseModelSerializer

User = get_user_model()


class SolicitudTransfusionSerializer(BaseModelSerializer):
    id_user = serializers.PrimaryKeyRelatedField(source="user", queryset=User.objects.all())
    id_paciente = serializers.PrimaryKeyRelatedField(source="paciente", queryset=Paciente.objects.all())
    id_medico = serializers.PrimaryKeyRelatedField(source="medico", queryset=Medico.objects.all())
    user_username = serializers.CharField(source="user.username", read_only=True)
    paciente_nombre = serializers.SerializerMethodField()
    medico_nombre = serializers.SerializerMethodField()

    class Meta:
        model = SolicitudTransfusion
        fields = [
            "nro",
            "fecha",
            "hora",
            "edad_valor",
            "edad_unidad",
            "fecha_nacimiento",
            "hto",
            "hb",
            "grupo",
            "hemocomponente",
            "cantidad",
            "fraccionado",
            "ml",
            "tipo_urgencia",
            "diagnostico",
            "id_user",
            "id_paciente",
            "id_medico",
            "user_username",
            "paciente_nombre",
            "medico_nombre",
            "created_at",
            "updated_at",
            "created_by",
        ]
        extra_kwargs = {
            "fecha_nacimiento": {"required": False, "allow_null": True},
            "ml": {"required": False, "allow_null": True},
        }
        service_class = SolicitudTransfusionValidationService
        read_only_fields = [
            "user_username",
            "paciente_nombre",
            "medico_nombre",
            "created_at",
            "updated_at",
            "created_by",
        ]

    def get_paciente_nombre(self, obj):
        return f"{obj.paciente.apellido_paterno} {obj.paciente.nombre}"

    def get_medico_nombre(self, obj):
        return f"{obj.medico.apellido_paterno} {obj.medico.nombre}"
