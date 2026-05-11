from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.admision.models import CitacionDonante, SolicitudTransfusion
from core.serializers import BaseModelSerializer

User = get_user_model()


class CitacionDonanteSerializer(BaseModelSerializer):
    nro_solicitud = serializers.PrimaryKeyRelatedField(
        source="solicitud",
        queryset=SolicitudTransfusion.objects.all(),
    )
    id_user = serializers.PrimaryKeyRelatedField(source="user", queryset=User.objects.all())
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = CitacionDonante
        fields = [
            "id",
            "nro_solicitud",
            "id_user",
            "user_username",
            "fecha",
            "servicio",
            "sala_cama",
            "cantidad",
            "codigo_donante",
            "hora",
            "grupo_factor",
            "tipo",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = ["id", "user_username", "created_at", "updated_at", "created_by"]
