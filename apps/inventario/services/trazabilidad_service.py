from django.core.exceptions import ValidationError

from apps.inventario.models import Trazabilidad
from core.services import (
    ChoiceValidationMixin,
    DateTimeBoliviaValidationMixin,
    HemocomponenteFechaIngresoValidationMixin,
    ValidationServiceMixin,
)


class TrazabilidadValidationService(
    ValidationServiceMixin,
    DateTimeBoliviaValidationMixin,
    ChoiceValidationMixin,
    HemocomponenteFechaIngresoValidationMixin,
):
    required_fields = ("hemocomponente", "evento", "encargado", "fecha_hora")

    @classmethod
    def validate_create(cls, attrs):
        errors = {}
        cls._capture_errors(errors, cls._validate_required, attrs, cls.required_fields)
        cls._capture_errors(errors, cls._validate_common_fields, attrs)

        if errors:
            raise ValidationError(errors)

    @classmethod
    def validate_update(cls, instance, attrs):
        errors = {}
        cls._capture_errors(errors, cls._validate_common_fields, attrs, instance)

        if errors:
            raise ValidationError(errors)

    @classmethod
    def _validate_common_fields(cls, attrs, instance=None):
        errors = {}

        if "evento" in attrs:
            cls._capture_errors(errors, cls._validate_choice, "evento", attrs.get("evento"), dict(Trazabilidad.EVENTO_CHOICES))

        if "fecha_hora" in attrs or instance is None:
            cls._capture_errors(errors, cls._validate_datetime_no_futuro, attrs, instance, "fecha_hora")

        if {"hemocomponente", "fecha_hora"}.intersection(attrs.keys()) or instance is None:
            cls._capture_errors(
                errors,
                cls._validate_fecha_desde_ingreso,
                attrs,
                instance,
                message="La fecha del evento no puede ser anterior al ingreso del hemocomponente.",
            )

        if errors:
            raise ValidationError(errors)
