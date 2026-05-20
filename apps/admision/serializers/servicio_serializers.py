from apps.admision.models import Servicio
from core.serializers import BaseModelSerializer


class ServicioSerializer(BaseModelSerializer):
    class Meta:
        model = Servicio
        fields = [
            "id",
            "nombre",
            "descripcion",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "created_by"]
