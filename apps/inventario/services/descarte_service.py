from django.core.exceptions import ValidationError

from apps.inventario.models import Descarte
from core.services import (
    ChoiceValidationMixin,
    DateTimeBoliviaValidationMixin,
    HemocomponenteFechaIngresoValidationMixin,
    RequiredTextValidationMixin,
    ValidationServiceMixin,
)


class DescarteValidationService(
    ValidationServiceMixin,
    DateTimeBoliviaValidationMixin,
    ChoiceValidationMixin,
    RequiredTextValidationMixin,
    HemocomponenteFechaIngresoValidationMixin,
):
    required_fields = ("hemocomponente", "tipo_accion", "fecha_hora")
    intercambio_hospital = "INTERCAMBIO_HOSPITAL"

    @classmethod
    def validate_create(cls, attrs):
        errors = {}
        cls._capture_errors(errors, cls._validate_required, attrs, cls.required_fields)
        cls._capture_errors(errors, cls._validate_common_fields, attrs)
        cls._capture_errors(errors, cls._validate_unique_hemocomponente, attrs)

        if errors:
            raise ValidationError(errors)

    @classmethod
    def validate_update(cls, instance, attrs):
        errors = {}
        cls._capture_errors(errors, cls._validate_common_fields, attrs, instance)
        cls._capture_errors(errors, cls._validate_unique_hemocomponente, attrs, instance)

        if errors:
            raise ValidationError(errors)

    @classmethod
    def _validate_common_fields(cls, attrs, instance=None):
        errors = {}

        if "tipo_accion" in attrs:
            cls._capture_errors(errors, cls._validate_choice, "tipo_accion", attrs.get("tipo_accion"), dict(Descarte.ACCION_CHOICES))

        if "motivo" in attrs and attrs.get("motivo") not in (None, ""):
            cls._capture_errors(errors, cls._validate_required_text, "motivo", attrs.get("motivo"))

        if {"tipo_accion", "hospital"}.intersection(attrs.keys()) or instance is None:
            cls._capture_errors(errors, cls._validate_hospital, attrs, instance)

        if "fecha_hora" in attrs or instance is None:
            cls._capture_errors(errors, cls._validate_datetime_no_futuro, attrs, instance, "fecha_hora")

        if {"hemocomponente", "fecha_hora"}.intersection(attrs.keys()) or instance is None:
            cls._capture_errors(
                errors,
                cls._validate_fecha_desde_ingreso,
                attrs,
                instance,
                message="La fecha de descarte no puede ser anterior al ingreso del hemocomponente.",
            )

        if errors:
            raise ValidationError(errors)

    @classmethod
    def _validate_unique_hemocomponente(cls, attrs, instance=None):
        hemocomponente = attrs.get("hemocomponente")
        if hemocomponente is None:
            return

        exists = Descarte.objects.filter(hemocomponente=hemocomponente)
        if instance is not None:
            exists = exists.exclude(pk=instance.pk)

        if exists.exists():
            raise ValidationError({"nro_bolsa": ["Ya existe un registro de descarte para este hemocomponente."]})

    @classmethod
    def _validate_hospital(cls, attrs, instance=None):
        tipo_accion = attrs.get("tipo_accion", getattr(instance, "tipo_accion", None))
        hospital = attrs.get("hospital", getattr(instance, "hospital", None))

        if tipo_accion == cls.intercambio_hospital:
            if hospital is None:
                raise ValidationError({"hospital": ["Seleccione el hospital de destino."]})
            return

        attrs["hospital"] = None
