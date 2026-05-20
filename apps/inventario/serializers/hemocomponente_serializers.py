from core.serializers import BaseModelSerializer
from apps.inventario.models import Hemocomponente
from apps.inventario.services import HemocomponenteValidationService


class HemocomponenteSerializer(BaseModelSerializer):
    class Meta:
        model = Hemocomponente
        service_class = HemocomponenteValidationService
        fields = [
            "nro_bolsa",
            "nro_tubuladura",
            "tipo",
            "grupo_sanguineo",
            "estado",
            "fecha_ingreso",
            "fecha_vencimiento",
            "devuelto",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = ["created_at", "updated_at", "created_by"]
