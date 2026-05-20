import re

from django.core.exceptions import ValidationError

from core.services import (
    DateTimeBoliviaValidationMixin,
    GrupoSanguineoValidationMixin,
    HemocomponenteFechaIngresoValidationMixin,
    PositivoNegativoValidationMixin,
    ReactivoValidationMixin,
    ValidationServiceMixin,
)


class PruebasPretransfHemaValidationService(
    ValidationServiceMixin,
    DateTimeBoliviaValidationMixin,
    ReactivoValidationMixin,
    PositivoNegativoValidationMixin,
    GrupoSanguineoValidationMixin,
    HemocomponenteFechaIngresoValidationMixin,
):
    bolsa_pattern = re.compile(r"^[A-Za-z0-9-]+$")
    reactivo_fields = ("anti_a", "anti_b", "anti_ab", "anti_d")
    positivo_negativo_fields = (
        "salina",
        "albumina",
        "liss",
        "coombs",
        "cruzada_mayor",
        "cruzada_menor",
        "hemolisis",
        "celula_a",
        "celula_b",
        "celula_o",
    )
    required_fields = (
        "fecha",
        "salina",
        "albumina",
        "liss",
        "coombs",
        "cruzada_mayor",
        "cruzada_menor",
        "hemolisis",
        "anti_a",
        "anti_b",
        "anti_ab",
        "anti_d",
        "celula_a",
        "celula_b",
        "celula_o",
        "fenotipo",
        "hemocomponente",
        "user",
        "solicitud",
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

        if "fecha" in attrs or instance is None:
            cls._capture_errors(errors, cls._validate_datetime_no_futuro, attrs, instance, "fecha")

        cls._capture_errors(errors, cls._validate_reactivo_fields, attrs, cls.reactivo_fields, instance)
        cls._capture_errors(errors, cls._validate_positivo_negativo_fields, attrs, cls.positivo_negativo_fields, instance)
        cls._capture_errors(errors, cls._validate_grupo_sanguineo_field, attrs, "fenotipo", instance)

        if {"hemocomponente", "fecha"}.intersection(attrs.keys()) or instance is None:
            cls._capture_errors(
                errors,
                cls._validate_fecha_desde_ingreso,
                attrs,
                instance,
                field="fecha",
                message="La fecha no puede ser anterior al ingreso del hemocomponente.",
            )

        if "hemocomponente" in attrs or instance is None:
            cls._capture_errors(errors, cls._validate_nro_bolsa, attrs, instance)

        if "solicitud" in attrs or instance is None:
            cls._capture_errors(errors, cls._validate_solicitud, attrs, instance)

        if errors:
            raise ValidationError(errors)

    @classmethod
    def _validate_nro_bolsa(cls, attrs, instance=None):
        hemocomponente = attrs.get("hemocomponente", getattr(instance, "hemocomponente", None))
        if hemocomponente is None:
            return

        nro_bolsa = str(hemocomponente.pk)
        if not cls.bolsa_pattern.fullmatch(nro_bolsa):
            raise ValidationError({"nro_bolsa": ["El nro de bolsa solo puede contener letras, numeros y guiones."]})

    @classmethod
    def _validate_solicitud(cls, attrs, instance=None):
        solicitud = attrs.get("solicitud", getattr(instance, "solicitud", None))
        if solicitud is None:
            return

        if not str(solicitud.nro).isdigit():
            raise ValidationError({"nro_solicitud": ["El nro de solicitud debe contener solo numeros."]})
