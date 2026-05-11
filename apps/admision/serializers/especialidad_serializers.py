from apps.admision.models import Especialidad
from core.serializers import BaseModelSerializer


class EspecialidadSerializer(BaseModelSerializer):
    class Meta:
        model = Especialidad
        fields = [
            "id",
            "nombre",
            "descripcion",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "created_by"]
