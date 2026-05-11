from rest_framework import serializers

from apps.admision.models import Especialidad, Medico
from core.serializers import BaseModelSerializer


class MedicoSerializer(BaseModelSerializer):
    especialidad = serializers.PrimaryKeyRelatedField(queryset=Especialidad.objects.all())
    especialidad_nombre = serializers.CharField(source="especialidad.nombre", read_only=True)

    class Meta:
        model = Medico
        fields = [
            "id",
            "especialidad",
            "especialidad_nombre",
            "matricula_profesional",
            "nombre",
            "apellido_paterno",
            "apellido_materno",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = ["id", "especialidad_nombre", "created_at", "updated_at", "created_by"]
