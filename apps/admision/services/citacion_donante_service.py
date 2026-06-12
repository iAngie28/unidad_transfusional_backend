import re

from django.core.exceptions import ValidationError

from apps.admision.models import CitacionDonante
from core.services import (
    ChoiceValidationMixin,
    FechaHoraBoliviaValidationMixin,
    PositiveIntegerValidationMixin,
    ValidationServiceMixin,
)


class CitacionDonanteValidationService(
    ValidationServiceMixin,
    FechaHoraBoliviaValidationMixin,
    ChoiceValidationMixin,
    PositiveIntegerValidationMixin,
):
    alphanumeric_pattern = re.compile(r"^[A-Za-z0-9]+$")
    text_number_space_pattern = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9 ]+$")

    @classmethod
    def validate_create(cls, attrs):
        errors = {}
        cls._capture_errors(
            errors,
            cls._validate_required,
            attrs,
            (
                "solicitud",
                "user",
                "fecha",
                "servicio",
                "cantidad",
                "hora",
                "grupo_factor",
                "tipo",
                "codigos_donante",
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

        solicitud = attrs.get("solicitud", getattr(instance, "solicitud", None))
        if solicitud is not None:
            cls._capture_errors(errors, cls._validate_nro_solicitud, solicitud)

        if "sala_cama" in attrs and attrs.get("sala_cama") not in (None, ""):
            cls._capture_errors(errors, cls._validate_sala_cama, attrs.get("sala_cama"))

        if "cantidad" in attrs:
            cls._capture_errors(errors, cls._validate_positive_integer, "cantidad", attrs.get("cantidad"))

        if "codigos_donante" in attrs:
            cls._capture_errors(errors, cls._validate_codigos_donante, attrs.get("codigos_donante"))

        if "grupo_factor" in attrs:
            cls._capture_errors(errors, cls._validate_choice, "grupo_factor", attrs.get("grupo_factor"), dict(CitacionDonante.GRUPO_CHOICES))

        if "tipo" in attrs:
            cls._capture_errors(errors, cls._validate_choice, "tipo", attrs.get("tipo"), dict(CitacionDonante.HEMOCOMPONENTE_CHOICES))

        if errors:
            raise ValidationError(errors)

    @classmethod
    def _validate_nro_solicitud(cls, solicitud):
        if not str(solicitud.nro).isdigit():
            raise ValidationError({"nro_solicitud": ["El nro de solicitud debe contener solo numeros."]})

    @classmethod
    def _validate_sala_cama(cls, value):
        if not cls.text_number_space_pattern.fullmatch(value):
            raise ValidationError({"sala_cama": ["Solo se permiten letras, numeros y espacios."]})

    @classmethod
    def _validate_codigos_donante(cls, codigos_list):
        if not isinstance(codigos_list, list):
            raise ValidationError({"codigos_donante": ["Debe ser una lista de códigos."]})
        if not codigos_list:
            raise ValidationError({"codigos_donante": ["Debe ingresar al menos un código de donante."]})
        for item in codigos_list:
            codigo = item.get("codigo", "")
            if not codigo:
                raise ValidationError({"codigos_donante": ["El código no puede estar vacío."]})
            if not cls.alphanumeric_pattern.fullmatch(str(codigo)):
                raise ValidationError({"codigos_donante": [f"El código '{codigo}' solo debe contener letras y números."]})
