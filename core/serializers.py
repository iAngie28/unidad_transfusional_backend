from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as DRFValidationError


class ServiceValidationMixin:
    """
    Ejecuta validaciones declaradas en una capa de servicios.

    Un serializer puede declarar `service_class` dentro de Meta. Si el servicio
    implementa `validate_create` o `validate_update`, este mixin lo invoca dentro
    del flujo normal de validacion de DRF.
    """

    def validate(self, attrs):
        attrs = super().validate(attrs)
        service_class = getattr(self.Meta, "service_class", None)

        if not service_class:
            return attrs

        try:
            if self.instance is not None and hasattr(service_class, "validate_update"):
                service_class.validate_update(self.instance, attrs)
            elif self.instance is None and hasattr(service_class, "validate_create"):
                service_class.validate_create(attrs)
        except DRFValidationError:
            raise
        except DjangoValidationError as exc:
            if hasattr(exc, "message_dict"):
                raise serializers.ValidationError(exc.message_dict)
            raise serializers.ValidationError(exc.messages)

        return attrs


class BaseModelSerializer(ServiceValidationMixin, serializers.ModelSerializer):
    """
    Serializador base del que heredarán todos los modelos del sistema.
    Aquí puedes agregar lógica global en el futuro.
    """
    pass
