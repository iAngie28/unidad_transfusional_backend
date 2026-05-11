from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.admision.models import Paciente, SolicitudTransfusion
from apps.laboratorio.models import PruebaPretransfusionalPAC
from core.serializers import BaseModelSerializer

User = get_user_model()


class PruebaPretransfusionalPACSerializer(BaseModelSerializer):
    paciente_id = serializers.PrimaryKeyRelatedField(source="paciente", queryset=Paciente.objects.all())
    user_id = serializers.PrimaryKeyRelatedField(source="user", queryset=User.objects.all())
    nro_solicitud = serializers.PrimaryKeyRelatedField(
        source="solicitud",
        queryset=SolicitudTransfusion.objects.all(),
    )
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = PruebaPretransfusionalPAC
        fields = [
            "id",
            "fecha_hora",
            "paciente_id",
            "user_id",
            "user_username",
            "nro_solicitud",
            "anti_a",
            "anti_b",
            "anti_ab",
            "anti_d",
            "control_rhesus",
            "alfa",
            "beta",
            "o",
            "fenotipo",
            "hto",
            "hb",
            "coombs_directo",
            "resultado",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = ["id", "user_username", "created_at", "updated_at", "created_by"]
