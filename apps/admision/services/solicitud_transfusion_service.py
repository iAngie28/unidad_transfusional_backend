from django.core.exceptions import ValidationError

from apps.admision.models import SolicitudTransfusion
from core.services import (
    BooleanValidationMixin,
    ChoiceValidationMixin,
    ClinicalValueValidationMixin,
    EdadValidationMixin,
    FechaHoraBoliviaValidationMixin,
    PositiveIntegerValidationMixin,
    RequiredTextValidationMixin,
    ValidationServiceMixin,
)


class SolicitudTransfusionValidationService(
    ValidationServiceMixin,
    EdadValidationMixin,
    FechaHoraBoliviaValidationMixin,
    ClinicalValueValidationMixin,
    RequiredTextValidationMixin,
    ChoiceValidationMixin,
    BooleanValidationMixin,
    PositiveIntegerValidationMixin,
):
    @classmethod
    def validate_create(cls, attrs):
        errors = {}
        cls._capture_errors(
            errors,
            cls._validate_required,
            attrs,
            (
                "fecha",
                "hora",
                "edad_valor",
                "edad_unidad",
                "hto",
                "hb",
                "grupo",
                "hemocomponente",
                "cantidad",
                "tipo_urgencia",
                "diagnostico",
            ),
        )
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

        cls._capture_errors(errors, cls._validate_fecha_hora_no_futura, attrs, instance)
        cls._capture_errors(errors, cls._validate_edad_fields, attrs, instance)
        cls._capture_errors(errors, cls._validate_clinical_values, attrs, instance)

        if "cantidad" in attrs:
            cls._capture_errors(errors, cls._validate_positive_integer, "cantidad", attrs.get("cantidad"))

        if "fraccionado" in attrs:
            cls._capture_errors(errors, cls._validate_boolean, "fraccionado", attrs.get("fraccionado"))

        if {"fraccionado", "ml", "cantidad"}.intersection(attrs.keys()) or instance is None:
            cls._capture_errors(errors, cls._validate_fraccionamiento, attrs, instance)

        if "diagnostico" in attrs:
            cls._capture_errors(errors, cls._validate_required_text, "diagnostico", attrs.get("diagnostico"))

        if "grupo" in attrs:
            cls._capture_errors(
                errors,
                cls._validate_choice,
                "grupo",
                attrs.get("grupo"),
                dict(SolicitudTransfusion.GRUPO_CHOICES),
            )

        if "hemocomponente" in attrs:
            cls._capture_errors(
                errors,
                cls._validate_choice,
                "hemocomponente",
                attrs.get("hemocomponente"),
                dict(SolicitudTransfusion.HEMOCOMPONENTE_CHOICES),
            )

        if "tipo_urgencia" in attrs:
            cls._capture_errors(
                errors,
                cls._validate_choice,
                "tipo_urgencia",
                attrs.get("tipo_urgencia"),
                dict(SolicitudTransfusion.URGENCIA_CHOICES),
            )

        if errors:
            raise ValidationError(errors)

    @classmethod
    def _validate_fraccionamiento(cls, attrs, instance=None):
        fraccionado = attrs.get("fraccionado", getattr(instance, "fraccionado", False))
        cantidad = attrs.get("cantidad", getattr(instance, "cantidad", None))
        ml_value = attrs.get("ml", getattr(instance, "ml", None))

        if not fraccionado:
            attrs["ml"] = None
            return

        attrs["cantidad"] = 1
        if cantidad not in (None, "", 1, "1"):
            raise ValidationError({"cantidad": ["Si la solicitud es fraccionada, la cantidad debe ser 1."]})

        if ml_value in (None, ""):
            raise ValidationError({"ml": ["Los ml son obligatorios si la solicitud es fraccionada."]})

        ml = cls._validate_positive_integer("ml", ml_value, max_value=1000)
        attrs["ml"] = ml
