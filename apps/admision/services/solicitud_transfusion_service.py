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
        # fraccionado y ml están deshabilitados en el modelo actual.
        # Esta función se conserva por compatibilidad pero no hace nada.
        pass
