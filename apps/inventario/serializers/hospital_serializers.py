from apps.inventario.models import Hospital
from core.serializers import BaseModelSerializer


class HospitalSerializer(BaseModelSerializer):
    class Meta:
        model = Hospital
        fields = [
            "id",
            "nombre",
            "descripcion",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "created_by"]
