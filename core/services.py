import math
import re
from datetime import date, datetime
from zoneinfo import ZoneInfo

from django.core.exceptions import ValidationError
from django.utils import timezone

BOLIVIA_TIMEZONE = ZoneInfo("America/La_Paz")
TEXT_NUMBER_SLASH_PATTERN = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9/ ]+$")
BLOOD_GROUP_CHOICES = ("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-")


class BaseService:
    model = None

    @classmethod
    def get_all(cls):
        return cls.model.objects.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.model.objects.filter(id=id).first()


class ValidationServiceMixin:
    @classmethod
    def _capture_errors(cls, errors, validator, *args, **kwargs):
        try:
            validator(*args, **kwargs)
        except ValidationError as exc:
            if hasattr(exc, "message_dict"):
                for field, messages in exc.message_dict.items():
                    errors.setdefault(field, []).extend(messages)
            else:
                errors.setdefault("non_field_errors", []).extend(exc.messages)

    @classmethod
    def _validate_required(cls, attrs, fields):
        errors = {}
        for field in fields:
            if attrs.get(field) in (None, ""):
                errors[field] = ["Este campo es obligatorio."]
        if errors:
            raise ValidationError(errors)


class EdadValidationMixin:
    edad_units = ("DIAS", "MESES", "ANOS")
    min_birth_date = date(1900, 1, 1)

    @classmethod
    def _validate_edad_fields(cls, attrs, instance=None):
        age_fields = {"edad_valor", "edad_unidad", "fecha_nacimiento"}
        if instance is not None and not age_fields.intersection(attrs.keys()):
            return

        errors = {}
        edad_valor = attrs.get("edad_valor", getattr(instance, "edad_valor", None))
        edad_unidad = attrs.get("edad_unidad", getattr(instance, "edad_unidad", None))
        fecha_nacimiento = attrs.get(
            "fecha_nacimiento",
            getattr(instance, "fecha_nacimiento", None),
        )

        edad_numero = None
        if edad_valor in (None, ""):
            errors["edad_valor"] = ["Este campo es obligatorio."]
        else:
            try:
                edad_numero = int(edad_valor)
            except (TypeError, ValueError):
                errors["edad_valor"] = ["La edad debe ser un numero entero positivo."]
            else:
                if edad_numero <= 0:
                    errors["edad_valor"] = ["La edad debe ser un numero positivo."]

        if edad_unidad in (None, ""):
            errors["edad_unidad"] = ["Este campo es obligatorio."]
        elif edad_unidad not in cls.edad_units:
            errors["edad_unidad"] = ["La unidad de edad debe ser DIAS, MESES o ANOS."]

        if edad_numero is not None and edad_unidad in cls.edad_units:
            max_value = cls._max_edad_value(edad_unidad)
            if edad_numero > max_value:
                errors["edad_valor"] = [
                    "La edad no puede indicar una fecha de nacimiento anterior a 1900 ni futura."
                ]

        if fecha_nacimiento not in (None, ""):
            today = datetime.now(BOLIVIA_TIMEZONE).date()
            if fecha_nacimiento > today:
                errors["fecha_nacimiento"] = ["La fecha de nacimiento no puede estar en el futuro."]
            elif fecha_nacimiento < cls.min_birth_date:
                errors["fecha_nacimiento"] = ["La fecha de nacimiento no puede ser anterior a 1900."]

        if errors:
            raise ValidationError(errors)

    @classmethod
    def _max_edad_value(cls, edad_unidad):
        today = datetime.now(BOLIVIA_TIMEZONE).date()
        if edad_unidad == "DIAS":
            return (today - cls.min_birth_date).days
        if edad_unidad == "MESES":
            return (today.year - cls.min_birth_date.year) * 12 + today.month - cls.min_birth_date.month
        return today.year - cls.min_birth_date.year


class FechaHoraBoliviaValidationMixin:
    bolivia_timezone = BOLIVIA_TIMEZONE

    @classmethod
    def _validate_fecha_hora_no_futura(cls, attrs, instance=None):
        datetime_fields = {"fecha", "hora"}
        if instance is not None and not datetime_fields.intersection(attrs.keys()):
            return

        errors = {}
        fecha = attrs.get("fecha", getattr(instance, "fecha", None))
        hora = attrs.get("hora", getattr(instance, "hora", None))
        now_bolivia = datetime.now(cls.bolivia_timezone)
        today_bolivia = now_bolivia.date()
        current_time_bolivia = now_bolivia.time().replace(microsecond=0)

        if fecha in (None, ""):
            errors["fecha"] = ["Este campo es obligatorio."]
        elif fecha > today_bolivia:
            errors["fecha"] = ["La fecha debe ser menor o igual a hoy."]

        if hora in (None, ""):
            errors["hora"] = ["Este campo es obligatorio."]
        elif fecha == today_bolivia and hora > current_time_bolivia:
            errors["hora"] = ["La hora debe ser menor o igual a la hora actual de Bolivia."]

        if errors:
            raise ValidationError(errors)


class FechaBoliviaValidationMixin:
    bolivia_timezone = BOLIVIA_TIMEZONE

    @classmethod
    def _validate_fecha_no_futura(cls, attrs, instance=None, field="fecha"):
        if instance is not None and field not in attrs:
            return

        value = attrs.get(field, getattr(instance, field, None))
        today_bolivia = datetime.now(cls.bolivia_timezone).date()

        if value in (None, ""):
            raise ValidationError({field: ["Este campo es obligatorio."]})
        if value > today_bolivia:
            raise ValidationError({field: ["La fecha debe ser menor o igual a hoy."]})


class DateTimeBoliviaValidationMixin:
    bolivia_timezone = BOLIVIA_TIMEZONE

    @classmethod
    def _to_bolivia_datetime(cls, value):
        if timezone.is_naive(value):
            value = timezone.make_aware(value, cls.bolivia_timezone)
        return value.astimezone(cls.bolivia_timezone)

    @classmethod
    def _validate_datetime_no_futuro(cls, attrs, instance=None, field="fecha_hora"):
        if instance is not None and field not in attrs:
            return

        value = attrs.get(field, getattr(instance, field, None))
        if value in (None, ""):
            raise ValidationError({field: ["Este campo es obligatorio."]})

        value_bolivia = cls._to_bolivia_datetime(value)
        now_bolivia = datetime.now(cls.bolivia_timezone)

        if value_bolivia > now_bolivia:
            raise ValidationError({field: ["La fecha y hora debe ser menor o igual a la actual en Bolivia."]})


class ChoiceValidationMixin:
    @classmethod
    def _validate_choice(cls, field, value, choices):
        if value in (None, ""):
            raise ValidationError({field: ["Este campo es obligatorio."]})
        if value not in choices:
            raise ValidationError({field: ["Seleccione una opcion valida."]})


class BooleanValidationMixin:
    @classmethod
    def _validate_boolean(cls, field, value):
        if not isinstance(value, bool):
            raise ValidationError({field: ["Debe ser un valor booleano."]})


class PositiveIntegerValidationMixin:
    @classmethod
    def _validate_positive_integer(cls, field, value, max_value=None):
        if value in (None, ""):
            raise ValidationError({field: ["Este campo es obligatorio."]})
        if isinstance(value, bool):
            raise ValidationError({field: ["Debe ser un numero entero positivo."]})
        if isinstance(value, float) and not value.is_integer():
            raise ValidationError({field: ["Debe ser un numero entero positivo."]})
        if isinstance(value, str) and not value.isdigit():
            raise ValidationError({field: ["Debe ser un numero entero positivo."]})

        try:
            integer_value = int(value)
        except (TypeError, ValueError):
            raise ValidationError({field: ["Debe ser un numero entero positivo."]})

        if integer_value <= 0:
            raise ValidationError({field: ["Debe ser mayor a cero."]})
        if max_value is not None and integer_value > max_value:
            raise ValidationError({field: [f"No puede ser mayor a {max_value}."]})

        return integer_value


class HemocomponenteFechaIngresoValidationMixin:
    @classmethod
    def _validate_fecha_desde_ingreso(
        cls,
        attrs,
        instance=None,
        field="fecha_hora",
        hemocomponente_field="hemocomponente",
        message=None,
    ):
        hemocomponente = attrs.get(hemocomponente_field, getattr(instance, hemocomponente_field, None))
        value = attrs.get(field, getattr(instance, field, None))

        if hemocomponente is None or value in (None, ""):
            return

        value_bolivia = cls._to_bolivia_datetime(value)
        fecha_ingreso = cls._to_bolivia_datetime(hemocomponente.fecha_ingreso)

        if value_bolivia < fecha_ingreso:
            raise ValidationError({
                field: [message or "La fecha no puede ser anterior al ingreso del hemocomponente."]
            })


class ClinicalValueValidationMixin:
    clinical_value_fields = ("hto", "hb")

    @classmethod
    def _validate_clinical_values(cls, attrs, instance=None, fields=None):
        fields = fields or cls.clinical_value_fields
        if instance is not None and not set(fields).intersection(attrs.keys()):
            return

        errors = {}
        for field in fields:
            if instance is not None and field not in attrs:
                continue

            validator = getattr(cls, f"_validate_{field}", None)
            if validator is None:
                continue

            value = attrs.get(field, getattr(instance, field, None))
            try:
                validator(value)
            except ValidationError as exc:
                if hasattr(exc, "message_dict"):
                    for error_field, messages in exc.message_dict.items():
                        errors.setdefault(error_field, []).extend(messages)
                else:
                    errors.setdefault(field, []).extend(exc.messages)

        if errors:
            raise ValidationError(errors)

    @classmethod
    def _validate_hto(cls, value):
        hto = cls._validate_float("hto", value)
        if hto < 0:
            raise ValidationError({"hto": ["El hematocrito no puede ser negativo."]})
        if hto >= 100:
            raise ValidationError({"hto": ["El hematocrito debe ser menor a 100%."]})

    @classmethod
    def _validate_hb(cls, value):
        hb = cls._validate_float("hb", value)
        if hb < 0:
            raise ValidationError({"hb": ["La hemoglobina no puede ser negativa."]})

    @classmethod
    def _validate_float(cls, field, value):
        if value in (None, ""):
            raise ValidationError({field: ["Este campo es obligatorio."]})
        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            raise ValidationError({field: ["Debe ser un numero valido."]})
        if not math.isfinite(numeric_value):
            raise ValidationError({field: ["Debe ser un numero valido."]})
        return numeric_value


class ReactivoValidationMixin:
    reactivo_choices = ("POSITIVO", "NEGATIVO")

    @classmethod
    def _validate_reactivo_fields(cls, attrs, fields, instance=None):
        errors = {}
        for field in fields:
            if instance is not None and field not in attrs:
                continue

            value = attrs.get(field, getattr(instance, field, None))
            if value in (None, ""):
                errors[field] = ["Este campo es obligatorio."]
            elif value not in cls.reactivo_choices:
                errors[field] = ["Seleccione una opcion valida."]

        if errors:
            raise ValidationError(errors)


class PositivoNegativoValidationMixin:
    positivo_negativo_choices = ("POSITIVO", "NEGATIVO")

    @classmethod
    def _validate_positivo_negativo_fields(cls, attrs, fields, instance=None):
        errors = {}
        for field in fields:
            if instance is not None and field not in attrs:
                continue

            value = attrs.get(field, getattr(instance, field, None))
            if value in (None, ""):
                errors[field] = ["Este campo es obligatorio."]
            elif value not in cls.positivo_negativo_choices:
                errors[field] = ["Seleccione POSITIVO o NEGATIVO."]

        if errors:
            raise ValidationError(errors)


class GrupoSanguineoValidationMixin:
    grupo_sanguineo_choices = BLOOD_GROUP_CHOICES

    @classmethod
    def _validate_grupo_sanguineo_field(cls, attrs, field="grupo", instance=None):
        if instance is not None and field not in attrs:
            return

        value = attrs.get(field, getattr(instance, field, None))
        if value in (None, ""):
            raise ValidationError({field: ["Este campo es obligatorio."]})
        if value not in cls.grupo_sanguineo_choices:
            raise ValidationError({field: ["Seleccione un grupo sanguineo valido."]})


class TextNumberSlashValidationMixin:
    text_number_slash_pattern = TEXT_NUMBER_SLASH_PATTERN

    @classmethod
    def _validate_text_number_slash(cls, field, value):
        if value in (None, ""):
            raise ValidationError({field: ["Este campo es obligatorio."]})
        if not isinstance(value, str):
            raise ValidationError({field: ["Debe ser texto."]})
        if not value.strip():
            raise ValidationError({field: ["Este campo no puede estar vacio."]})
        if not cls.text_number_slash_pattern.fullmatch(value):
            raise ValidationError({field: ["Solo se permiten letras, numeros, espacios y /."]})


class RequiredTextValidationMixin:
    @classmethod
    def _validate_required_text(cls, field, value):
        if value in (None, ""):
            raise ValidationError({field: ["Este campo es obligatorio."]})
        if not isinstance(value, str):
            raise ValidationError({field: ["Debe ser texto."]})
        if not value.strip():
            raise ValidationError({field: ["Este campo no puede estar vacio."]})
