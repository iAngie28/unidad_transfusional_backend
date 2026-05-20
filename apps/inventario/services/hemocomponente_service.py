import re

from django.core.exceptions import ValidationError

from apps.inventario.models import Hemocomponente
from core.services import (
    BooleanValidationMixin,
    ChoiceValidationMixin,
    DateTimeBoliviaValidationMixin,
    ValidationServiceMixin,
)


class HemocomponenteValidationService(
    ValidationServiceMixin,
    DateTimeBoliviaValidationMixin,
    ChoiceValidationMixin,
    BooleanValidationMixin,
):
    identifier_pattern = re.compile(r"^[A-Za-z0-9-]+$")
    required_fields = (
        "nro_bolsa",
        "nro_tubuladura",
        "tipo",
        "grupo_sanguineo",
        "estado",
        "fecha_ingreso",
        "fecha_vencimiento",
    )

    @classmethod
    def validate_create(cls, attrs):
        errors = {}
        cls._capture_errors(errors, cls._validate_required, attrs, cls.required_fields)
        cls._capture_errors(errors, cls._validate_common_fields, attrs)
        cls._capture_errors(errors, cls._validate_unique_fields, attrs)

        if errors:
            raise ValidationError(errors)

    @classmethod
    def validate_update(cls, instance, attrs):
        errors = {}
        cls._capture_errors(errors, cls._validate_common_fields, attrs, instance)
        cls._capture_errors(errors, cls._validate_unique_fields, attrs, instance)

        if errors:
            raise ValidationError(errors)

    @classmethod
    def _validate_common_fields(cls, attrs, instance=None):
        errors = {}

        if "nro_bolsa" in attrs:
            cls._capture_errors(errors, cls._validate_identifier, "nro_bolsa", attrs.get("nro_bolsa"))

        if "nro_tubuladura" in attrs:
            cls._capture_errors(errors, cls._validate_identifier, "nro_tubuladura", attrs.get("nro_tubuladura"))

        if "tipo" in attrs:
            cls._capture_errors(errors, cls._validate_choice, "tipo", attrs.get("tipo"), dict(Hemocomponente.TIPO_CHOICES))

        if "grupo_sanguineo" in attrs:
            cls._capture_errors(
                errors,
                cls._validate_choice,
                "grupo_sanguineo",
                attrs.get("grupo_sanguineo"),
                dict(Hemocomponente.GRUPO_CHOICES),
            )

        if "estado" in attrs:
            cls._capture_errors(errors, cls._validate_choice, "estado", attrs.get("estado"), dict(Hemocomponente.ESTADO_CHOICES))

        if "fecha_ingreso" in attrs or instance is None:
            cls._capture_errors(errors, cls._validate_datetime_no_futuro, attrs, instance, "fecha_ingreso")

        if {"fecha_ingreso", "fecha_vencimiento"}.intersection(attrs.keys()) or instance is None:
            cls._capture_errors(errors, cls._validate_fecha_vencimiento, attrs, instance)

        if "devuelto" in attrs:
            cls._capture_errors(errors, cls._validate_boolean, "devuelto", attrs.get("devuelto"))

        if errors:
            raise ValidationError(errors)

    @classmethod
    def _validate_identifier(cls, field, value):
        if value in (None, ""):
            raise ValidationError({field: ["Este campo es obligatorio."]})
        if not cls.identifier_pattern.fullmatch(str(value)):
            raise ValidationError({field: ["Solo se permiten letras, numeros y guiones."]})

    @classmethod
    def _validate_unique_fields(cls, attrs, instance=None):
        errors = {}

        nro_bolsa = attrs.get("nro_bolsa")
        if nro_bolsa not in (None, ""):
            exists = Hemocomponente.objects.filter(nro_bolsa=nro_bolsa)
            if instance is not None:
                exists = exists.exclude(pk=instance.pk)
            if exists.exists():
                errors["nro_bolsa"] = ["Ya existe un hemocomponente con este nro de bolsa."]

        nro_tubuladura = attrs.get("nro_tubuladura")
        if nro_tubuladura not in (None, ""):
            exists = Hemocomponente.objects.filter(nro_tubuladura=nro_tubuladura)
            if instance is not None:
                exists = exists.exclude(pk=instance.pk)
            if exists.exists():
                errors["nro_tubuladura"] = ["Ya existe un hemocomponente con este nro de tubuladura."]

        if errors:
            raise ValidationError(errors)

    @classmethod
    def _validate_fecha_vencimiento(cls, attrs, instance=None):
        fecha_ingreso = attrs.get("fecha_ingreso", getattr(instance, "fecha_ingreso", None))
        fecha_vencimiento = attrs.get("fecha_vencimiento", getattr(instance, "fecha_vencimiento", None))

        if fecha_vencimiento in (None, ""):
            raise ValidationError({"fecha_vencimiento": ["Este campo es obligatorio."]})
        if fecha_ingreso in (None, ""):
            raise ValidationError({"fecha_ingreso": ["Este campo es obligatorio."]})

        fecha_ingreso = cls._to_bolivia_datetime(fecha_ingreso)
        fecha_vencimiento = cls._to_bolivia_datetime(fecha_vencimiento)

        if fecha_vencimiento <= fecha_ingreso:
            raise ValidationError({"fecha_vencimiento": ["La fecha de vencimiento debe ser posterior a la fecha de ingreso."]})
