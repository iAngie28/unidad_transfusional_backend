import re

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.admision.models import Paciente
from core.services import EdadValidationMixin, ValidationServiceMixin


class PacienteValidationService(ValidationServiceMixin, EdadValidationMixin):
    name_pattern = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+$")

    @classmethod
    def validate_create(cls, attrs):
        errors = {}
        cls._capture_errors(
            errors,
            cls._validate_required,
            attrs,
            (
                "ci",
                "nombre",
                "apellido_paterno",
                "edad_valor",
                "edad_unidad",
                "historia_clinica",
                "grupo_sanguineo",
            ),
        )

        if "ci" not in errors:
            cls._capture_errors(errors, cls._validate_ci, attrs.get("ci"))
            if "ci" not in errors:
                cls._capture_errors(errors, cls._validate_ci_unique, attrs.get("ci"))

        cls._capture_errors(errors, cls._validate_common_fields, attrs)

        if "historia_clinica" not in errors:
            cls._capture_errors(
                errors,
                cls._validate_historia_clinica_unique,
                attrs.get("historia_clinica"),
            )

        if errors:
            raise ValidationError(errors)

    @classmethod
    def validate_update(cls, instance, attrs):
        errors = {}

        if "ci" in attrs:
            cls._capture_errors(errors, cls._validate_ci, attrs.get("ci"))
            if "ci" not in errors:
                cls._capture_errors(errors, cls._validate_ci_unique, attrs.get("ci"), instance=instance)

        cls._capture_errors(errors, cls._validate_common_fields, attrs, instance)

        if "historia_clinica" in attrs:
            cls._capture_errors(
                errors,
                cls._validate_historia_clinica_unique,
                attrs.get("historia_clinica"),
                instance=instance,
            )

        if errors:
            raise ValidationError(errors)

    @classmethod
    def _validate_common_fields(cls, attrs, instance=None):
        errors = {}

        for field in ("nombre", "apellido_paterno"):
            if field in attrs:
                cls._capture_errors(errors, cls._validate_person_name, field, attrs.get(field))

        if attrs.get("apellido_materno"):
            cls._capture_errors(errors, cls._validate_person_name, "apellido_materno", attrs.get("apellido_materno"))

        cls._capture_errors(errors, cls._validate_edad_fields, attrs, instance)

        if "sexo" in attrs:
            cls._capture_errors(errors, cls._validate_sexo, attrs.get("sexo"))

        if errors:
            raise ValidationError(errors)

    @classmethod
    def _validate_ci(cls, value):
        if value in (None, ""):
            raise ValidationError({"ci": ["Este campo es obligatorio."]})
        if not str(value).isdigit():
            raise ValidationError({"ci": ["El CI debe contener solo numeros."]})

    @classmethod
    def _validate_ci_unique(cls, value, instance=None):
        queryset = Paciente.objects.filter(ci=value)
        if instance is not None:
            queryset = queryset.exclude(pk=instance.pk)
        if queryset.exists():
            raise ValidationError({"ci": ["Este CI ya esta registrado."]})

    @classmethod
    def _validate_person_name(cls, field, value):
        if value in (None, ""):
            raise ValidationError({field: ["Este campo es obligatorio."]})
        if not cls.name_pattern.fullmatch(value):
            raise ValidationError({
                field: ["Solo se permiten letras y espacios. No uses numeros ni caracteres especiales."]
            })

    @classmethod
    def _validate_sexo(cls, value):
        if value in (None, ""):
            return
        if value not in (Paciente.SEXO_MASCULINO, Paciente.SEXO_FEMENINO):
            raise ValidationError({"sexo": ["El sexo debe ser M o F."]})

    @classmethod
    def _validate_historia_clinica_unique(cls, value, instance=None):
        queryset = Paciente.objects.filter(historia_clinica=value)
        if instance is not None:
            queryset = queryset.exclude(pk=instance.pk)
        if queryset.exists():
            raise ValidationError({"historia_clinica": ["Esta historia clinica ya esta registrada."]})


class PacienteService:
    @staticmethod
    @transaction.atomic
    def registrar_grupo_sanguineo(ci, datos_grupo, usuario=None):
        grupo_sanguineo = datos_grupo.get("grupo_sanguineo")

        if not grupo_sanguineo:
            grupo_celular = datos_grupo.get("grupo_celular")
            factor_rh = datos_grupo.get("factor_rh")
            if grupo_celular and factor_rh:
                grupo_sanguineo = f"{grupo_celular}{factor_rh}"

        if not grupo_sanguineo:
            raise ValueError("Debe enviar grupo_sanguineo o grupo_celular con factor_rh.")

        paciente = Paciente.objects.select_for_update().get(ci=ci)
        paciente.grupo_sanguineo = grupo_sanguineo
        if usuario is not None:
            paciente.created_by = paciente.created_by or usuario
        paciente.save(update_fields=["grupo_sanguineo", "created_by", "updated_at"])
        return paciente
