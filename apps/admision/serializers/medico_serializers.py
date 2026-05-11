from core.serializers import BaseModelSerializer
from apps.admision.models import Medico


class MedicoSerializer(BaseModelSerializer):
    class Meta:
        model = Medico
        fields = [
            "id",
            "especialidad",
            "matricula_profesional",
            "nombre",
            "apellido_paterno",
            "apellido_materno",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "created_by"]
