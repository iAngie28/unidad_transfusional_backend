from core.serializers import BaseModelSerializer
from apps.admision.models import Paciente
from apps.admision.services import PacienteValidationService


class PacienteSerializer(BaseModelSerializer):
    class Meta:
        model = Paciente
        fields = [
            "ci",
            "nombre",
            "apellido_paterno",
            "apellido_materno",
            "edad_valor",
            "edad_unidad",
            "fecha_nacimiento",
            "sexo",
            "historia_clinica",
            "grupo_sanguineo",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = ["created_at", "updated_at", "created_by"]
        extra_kwargs = {
            "ci": {"validators": []},
            "historia_clinica": {"validators": []},
            "sexo": {"required": False, "allow_null": True, "allow_blank": True},
            "fecha_nacimiento": {"required": False, "allow_null": True},
        }
        service_class = PacienteValidationService
