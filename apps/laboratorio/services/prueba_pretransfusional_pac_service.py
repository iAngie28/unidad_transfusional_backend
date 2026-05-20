from django.core.exceptions import ValidationError

from core.services import (
    ClinicalValueValidationMixin,
    DateTimeBoliviaValidationMixin,
    GrupoSanguineoValidationMixin,
    PositivoNegativoValidationMixin,
    ReactivoValidationMixin,
    TextNumberSlashValidationMixin,
    ValidationServiceMixin,
)


class PruebaPretransfusionalPACValidationService(
    ValidationServiceMixin,
    DateTimeBoliviaValidationMixin,
    ReactivoValidationMixin,
    PositivoNegativoValidationMixin,
    GrupoSanguineoValidationMixin,
    ClinicalValueValidationMixin,
    TextNumberSlashValidationMixin,
):
    reactivo_fields = ("anti_a", "anti_b", "anti_ab", "anti_d")
    positivo_negativo_fields = ("control_rhesus", "alfa", "beta", "o", "coombs_directo")
    required_fields = (
        "fecha_hora",
        "paciente",
        "user",
        "solicitud",
        "anti_a",
        "anti_b",
        "anti_ab",
        "anti_d",
        "control_rhesus",
        "alfa",
        "beta",
        "o",
        "fenotipo",
        "hto",
        "hb",
        "coombs_directo",
        "resultado",
    )

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

        if "fecha_hora" in attrs or instance is None:
            cls._capture_errors(errors, cls._validate_datetime_no_futuro, attrs, instance, "fecha_hora")

        cls._capture_errors(errors, cls._validate_reactivo_fields, attrs, cls.reactivo_fields, instance)
        cls._capture_errors(errors, cls._validate_positivo_negativo_fields, attrs, cls.positivo_negativo_fields, instance)
        cls._capture_errors(errors, cls._validate_grupo_sanguineo_field, attrs, "fenotipo", instance)
        cls._capture_errors(errors, cls._validate_clinical_values, attrs, instance)

        if "resultado" in attrs:
            cls._capture_errors(errors, cls._validate_text_number_slash, "resultado", attrs.get("resultado"))

        if {"paciente", "solicitud"}.intersection(attrs.keys()) or instance is None:
            cls._capture_errors(errors, cls._validate_solicitud_paciente, attrs, instance)

        if errors:
            raise ValidationError(errors)

    @classmethod
    def _validate_solicitud_paciente(cls, attrs, instance=None):
        paciente = attrs.get("paciente", getattr(instance, "paciente", None))
        solicitud = attrs.get("solicitud", getattr(instance, "solicitud", None))

        if paciente is None or solicitud is None:
            return

        if solicitud.paciente_id != paciente.pk:
            raise ValidationError({"nro_solicitud": ["La solicitud seleccionada no pertenece al paciente."]})
