from datetime import datetime

from django.core.exceptions import ValidationError
from django.db.models import Sum

from apps.laboratorio.models import Transfusion
from core.services import (
    BooleanValidationMixin,
    ChoiceValidationMixin,
    DateTimeBoliviaValidationMixin,
    PositiveIntegerValidationMixin,
    RequiredTextValidationMixin,
    ValidationServiceMixin,
)


class TransfusionValidationService(
    ValidationServiceMixin,
    DateTimeBoliviaValidationMixin,
    RequiredTextValidationMixin,
    ChoiceValidationMixin,
    BooleanValidationMixin,
    PositiveIntegerValidationMixin,
):
    max_ml_por_bolsa = 1000
    required_fields = (
        "servicio",
        "diagnostico",
        "grupo_cabecera_h",
        "hora_inicio",
        "fraccionado",
        "hemocomponente",
        "paciente",
        "user",
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

        if "diagnostico" in attrs:
            cls._capture_errors(errors, cls._validate_required_text, "diagnostico", attrs.get("diagnostico"))

        if "grupo_cabecera_h" in attrs:
            cls._capture_errors(errors, cls._validate_choice, "grupo_cabecera_h", attrs.get("grupo_cabecera_h"), dict(Transfusion.GRUPO_CHOICES))

        if "hora_inicio" in attrs or instance is None:
            cls._capture_errors(errors, cls._validate_datetime_no_futuro, attrs, instance, "hora_inicio")

        if {"hora_inicio", "hora_fin"}.intersection(attrs.keys()) or instance is None:
            cls._capture_errors(errors, cls._validate_horas, attrs, instance)

        if "fraccionado" in attrs:
            cls._capture_errors(errors, cls._validate_boolean, "fraccionado", attrs.get("fraccionado"))

        if {"ml", "fraccionado", "hemocomponente"}.intersection(attrs.keys()) or instance is None:
            cls._capture_errors(errors, cls._validate_ml, attrs, instance)

        if errors:
            raise ValidationError(errors)

    @classmethod
    def _validate_horas(cls, attrs, instance=None):
        hora_inicio = attrs.get("hora_inicio", getattr(instance, "hora_inicio", None))
        hora_fin = attrs.get("hora_fin", getattr(instance, "hora_fin", None))

        if hora_inicio in (None, ""):
            raise ValidationError({"hora_inicio": ["Este campo es obligatorio."]})
        if hora_fin in (None, ""):
            return

        hora_inicio = cls._to_bolivia_datetime(hora_inicio)
        hora_fin = cls._to_bolivia_datetime(hora_fin)
        now_bolivia = datetime.now(cls.bolivia_timezone)

        if hora_fin < hora_inicio:
            raise ValidationError({"hora_fin": ["La hora de fin no puede ser anterior a la hora de inicio."]})
        if hora_fin > now_bolivia:
            raise ValidationError({"hora_fin": ["La hora de fin debe ser menor o igual a la actual en Bolivia."]})

    @classmethod
    def _validate_ml(cls, attrs, instance=None):
        hemocomponente = attrs.get("hemocomponente", getattr(instance, "hemocomponente", None))
        fraccionado = attrs.get("fraccionado", getattr(instance, "fraccionado", False))
        value = attrs.get("ml", getattr(instance, "ml", cls.max_ml_por_bolsa))

        if not fraccionado:
            value = cls.max_ml_por_bolsa
            attrs["ml"] = cls.max_ml_por_bolsa

        ml = cls._validate_positive_integer("ml", value, max_value=cls.max_ml_por_bolsa)

        if hemocomponente is None:
            return

        transfusiones = Transfusion.objects.filter(hemocomponente=hemocomponente)
        if instance is not None:
            transfusiones = transfusiones.exclude(pk=instance.pk)

        total_usado = transfusiones.aggregate(total=Sum("ml"))["total"] or 0
        if total_usado + ml > cls.max_ml_por_bolsa:
            disponible = cls.max_ml_por_bolsa - total_usado
            raise ValidationError({"ml": [f"La bolsa solo tiene {disponible} ml disponibles."]})
