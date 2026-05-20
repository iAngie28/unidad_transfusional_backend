import re

from django.core.exceptions import ValidationError

from core.services import FechaBoliviaValidationMixin, ValidationServiceMixin


class ConsentimientoInformadoValidationService(ValidationServiceMixin, FechaBoliviaValidationMixin):
    name_pattern = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+$")

    @classmethod
    def validate_create(cls, attrs):
        errors = {}
        cls._capture_errors(
            errors,
            cls._validate_required,
            attrs,
            (
                "solicitud",
                "fecha",
                "servicio",
                "nombre_familiar",
                "apellido_paterno_familiar",
                "telefono",
                "ci",
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

        cls._capture_errors(errors, cls._validate_fecha_no_futura, attrs, instance)

        for field in ("nombre_familiar", "apellido_paterno_familiar"):
            if field in attrs:
                cls._capture_errors(errors, cls._validate_person_name, field, attrs.get(field))

        if attrs.get("apellido_materno_familiar"):
            cls._capture_errors(
                errors,
                cls._validate_person_name,
                "apellido_materno_familiar",
                attrs.get("apellido_materno_familiar"),
            )

        if "telefono" in attrs:
            cls._capture_errors(errors, cls._validate_numeric_only, "telefono", attrs.get("telefono"))

        if "ci" in attrs:
            cls._capture_errors(errors, cls._validate_numeric_only, "ci", attrs.get("ci"))

        if errors:
            raise ValidationError(errors)

    @classmethod
    def _validate_person_name(cls, field, value):
        if value in (None, "") or not str(value).strip():
            raise ValidationError({field: ["Este campo es obligatorio."]})
        if not cls.name_pattern.fullmatch(value):
            raise ValidationError({field: ["Solo se permiten letras y espacios."]})

    @classmethod
    def _validate_numeric_only(cls, field, value):
        if value in (None, ""):
            raise ValidationError({field: ["Este campo es obligatorio."]})
        if not str(value).isdigit():
            raise ValidationError({field: ["Debe contener solo numeros."]})
