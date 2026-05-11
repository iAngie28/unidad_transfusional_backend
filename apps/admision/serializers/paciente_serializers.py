from core.serializers import BaseModelSerializer
from apps.admision.models import Paciente


class PacienteSerializer(BaseModelSerializer):
    class Meta:
        model = Paciente
        fields = [
            "ci",
            "nombre",
            "apellido_paterno",
            "apellido_materno",
            "edad",
            "sexo",
            "historia_clinica",
            "grupo_sanguineo",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = ["created_at", "updated_at", "created_by"]
