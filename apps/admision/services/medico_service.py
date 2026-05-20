import re

from django.core.exceptions import ValidationError

from apps.admision.models import Especialidad, Medico
from core.services import ValidationServiceMixin


class MedicoValidationService(ValidationServiceMixin):
    name_pattern = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+$")

    @classmethod
    def validate_create(cls, attrs):
        errors = {}
        cls._capture_errors(
            errors,
            cls._validate_required,
            attrs,
            ("especialidad", "matricula_profesional", "nombre", "apellido_paterno"),
        )

        cls._capture_errors(errors, cls._validate_common_fields, attrs)

        if "matricula_profesional" not in errors:
            cls._capture_errors(
                errors,
                cls._validate_matricula_unique,
                attrs.get("matricula_profesional"),
            )

        if errors:
            raise ValidationError(errors)

    @classmethod
    def validate_update(cls, instance, attrs):
        errors = {}
        cls._capture_errors(errors, cls._validate_common_fields, attrs)

        if "matricula_profesional" in attrs and "matricula_profesional" not in errors:
            cls._capture_errors(
                errors,
                cls._validate_matricula_unique,
                attrs.get("matricula_profesional"),
                instance=instance,
            )

        if errors:
            raise ValidationError(errors)

    @classmethod
    def _validate_common_fields(cls, attrs):
        errors = {}

        if "especialidad" in attrs:
            cls._capture_errors(errors, cls._validate_especialidad, attrs.get("especialidad"))

        for field in ("nombre", "apellido_paterno"):
            if field in attrs:
                cls._capture_errors(errors, cls._validate_person_name, field, attrs.get(field))

        if attrs.get("apellido_materno"):
            cls._capture_errors(errors, cls._validate_person_name, "apellido_materno", attrs.get("apellido_materno"))

        if errors:
            raise ValidationError(errors)

    @classmethod
    def _validate_especialidad(cls, value):
        if value in (None, ""):
            raise ValidationError({"especialidad": ["Este campo es obligatorio."]})

        if isinstance(value, Especialidad):
            if not Especialidad.objects.filter(pk=value.pk).exists():
                raise ValidationError({"especialidad": ["La especialidad seleccionada no existe."]})
            return

        if not Especialidad.objects.filter(pk=value).exists():
            raise ValidationError({"especialidad": ["La especialidad seleccionada no existe."]})

    @classmethod
    def _validate_matricula_unique(cls, value, instance=None):
        if value in (None, ""):
            raise ValidationError({"matricula_profesional": ["Este campo es obligatorio."]})

        queryset = Medico.objects.filter(matricula_profesional=value)
        if instance is not None:
            queryset = queryset.exclude(pk=instance.pk)
        if queryset.exists():
            raise ValidationError({"matricula_profesional": ["Esta matricula profesional ya esta registrada."]})

    @classmethod
    def _validate_person_name(cls, field, value):
        if value in (None, ""):
            raise ValidationError({field: ["Este campo es obligatorio."]})

        if not cls.name_pattern.fullmatch(value):
            raise ValidationError({
                field: ["Solo se permiten letras mayusculas, minusculas, ñ y espacios."]
            })
