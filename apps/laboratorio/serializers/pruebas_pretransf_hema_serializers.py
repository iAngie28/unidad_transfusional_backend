from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.admision.models import SolicitudTransfusion
from apps.inventario.models import Hemocomponente
from apps.laboratorio.models import PruebasPretransfHema
from core.serializers import BaseModelSerializer

User = get_user_model()


class PruebasPretransfHemaSerializer(BaseModelSerializer):
    nro_bolsa = serializers.PrimaryKeyRelatedField(
        source="hemocomponente",
        queryset=Hemocomponente.objects.all(),
    )
    user_id = serializers.PrimaryKeyRelatedField(source="user", queryset=User.objects.all())
    nro_solicitud = serializers.PrimaryKeyRelatedField(
        source="solicitud",
        queryset=SolicitudTransfusion.objects.all(),
    )
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = PruebasPretransfHema
        fields = [
            "id",
            "fecha",
            "salina",
            "albumina",
            "liss",
            "coombs",
            "cruzada_mayor",
            "cruzada_menor",
            "hemolisis",
            "anti_a",
            "anti_b",
            "anti_ab",
            "anti_d",
            "celula_a",
            "celula_b",
            "celula_o",
            "fenotipo",
            "nro_bolsa",
            "user_id",
            "user_username",
            "nro_solicitud",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = ["id", "user_username", "created_at", "updated_at", "created_by"]
