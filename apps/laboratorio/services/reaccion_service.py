from django.core.exceptions import ValidationError

from core.services import DateTimeBoliviaValidationMixin, RequiredTextValidationMixin, ValidationServiceMixin


class ReaccionValidationService(
    ValidationServiceMixin,
    DateTimeBoliviaValidationMixin,
    RequiredTextValidationMixin,
):
    required_fields = ("transfusion", "descripcion", "fecha_hora")

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

        if "descripcion" in attrs:
            cls._capture_errors(errors, cls._validate_required_text, "descripcion", attrs.get("descripcion"))

        if "fecha_hora" in attrs or instance is None:
            cls._capture_errors(errors, cls._validate_datetime_no_futuro, attrs, instance, "fecha_hora")

        if {"transfusion", "fecha_hora"}.intersection(attrs.keys()) or instance is None:
            cls._capture_errors(errors, cls._validate_fecha_transfusion, attrs, instance)

        if errors:
            raise ValidationError(errors)

    @classmethod
    def _validate_fecha_transfusion(cls, attrs, instance=None):
        transfusion = attrs.get("transfusion", getattr(instance, "transfusion", None))
        fecha_hora = attrs.get("fecha_hora", getattr(instance, "fecha_hora", None))

        if transfusion is None or fecha_hora in (None, ""):
            return

        fecha_reaccion = cls._to_bolivia_datetime(fecha_hora)
        hora_inicio = cls._to_bolivia_datetime(transfusion.hora_inicio)

        if fecha_reaccion < hora_inicio:
            raise ValidationError({
                "fecha_hora": ["La fecha y hora de la reaccion no puede ser anterior al inicio de la transfusion."]
            })

        if transfusion.hora_fin:
            hora_fin = cls._to_bolivia_datetime(transfusion.hora_fin)
            if fecha_reaccion > hora_fin:
                raise ValidationError({
                    "fecha_hora": ["La fecha y hora de la reaccion no puede ser posterior al fin de la transfusion."]
                })
