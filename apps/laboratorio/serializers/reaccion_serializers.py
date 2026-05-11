from rest_framework import serializers

from apps.laboratorio.models import Reaccion, Transfusion
from core.serializers import BaseModelSerializer


class ReaccionSerializer(BaseModelSerializer):
    id_transfusion = serializers.PrimaryKeyRelatedField(
        source="transfusion",
        queryset=Transfusion.objects.all(),
    )

    class Meta:
        model = Reaccion
        fields = [
            "id",
            "id_transfusion",
            "descripcion",
            "fecha_hora",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "created_by"]
