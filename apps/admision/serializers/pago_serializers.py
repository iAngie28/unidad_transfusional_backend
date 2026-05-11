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
    nro_solicitud = serializers.CharField(source="citacion.solicitud_id", read_only=True)
    id_transfusion = serializers.PrimaryKeyRelatedField(
        source="transfusion",
        queryset=Transfusion.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Pago
        fields = [
            "id",
            "estado",
            "es_sus",
            "id_citacion",
            "nro_solicitud",
            "id_transfusion",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = ["id", "nro_solicitud", "created_at", "updated_at", "created_by"]
