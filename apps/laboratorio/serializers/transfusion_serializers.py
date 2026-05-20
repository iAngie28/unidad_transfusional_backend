from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.admision.models import Paciente, Servicio
from apps.inventario.models import Hemocomponente
from apps.laboratorio.models import Transfusion
from apps.laboratorio.services import TransfusionValidationService
from core.serializers import BaseModelSerializer

User = get_user_model()


class TransfusionSerializer(BaseModelSerializer):
    nro_bolsa = serializers.PrimaryKeyRelatedField(
        source="hemocomponente",
        queryset=Hemocomponente.objects.all(),
    )
    ci_paciente = serializers.PrimaryKeyRelatedField(source="paciente", queryset=Paciente.objects.all())
    user_id = serializers.PrimaryKeyRelatedField(source="user", queryset=User.objects.all())
    id_servicio = serializers.PrimaryKeyRelatedField(source="servicio", queryset=Servicio.objects.all())
    servicio_nombre = serializers.CharField(source="servicio.nombre", read_only=True)
    paciente_nombre = serializers.SerializerMethodField()
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Transfusion
        service_class = TransfusionValidationService
        fields = [
            "id",
            "id_servicio",
            "servicio_nombre",
            "diagnostico",
            "ate_trans_alerg",
            "grupo_cabecera_h",
            "hora_inicio",
            "hora_fin",
            "fraccionado",
            "ml",
            "nro_bolsa",
            "ci_paciente",
            "paciente_nombre",
            "user_id",
            "user_username",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = ["id", "servicio_nombre", "paciente_nombre", "user_username", "created_at", "updated_at", "created_by"]

    def get_paciente_nombre(self, obj):
        return f"{obj.paciente.apellido_paterno} {obj.paciente.nombre}"
