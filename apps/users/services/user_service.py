import re

from django.contrib.auth import password_validation
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from apps.users.models import User
from core.services import ValidationServiceMixin


class UserValidationService(ValidationServiceMixin):
    name_pattern = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+$")
    username_validator = UnicodeUsernameValidator()

    @classmethod
    def validate_create(cls, attrs):
        errors = {}
        cls._capture_errors(
            errors,
            cls._validate_required,
            attrs,
            ("username", "password", "first_name", "last_name", "rol"),
        )

        if "username" not in errors:
            cls._capture_errors(errors, cls._validate_username, attrs.get("username"))
        if "username" not in errors:
            cls._capture_errors(errors, cls._validate_username_unique, attrs.get("username"))

        cls._capture_errors(errors, cls._validate_common_fields, attrs)

        if "password" not in errors:
            cls._capture_errors(errors, cls._validate_password, attrs.get("password"), attrs)

        if errors:
            raise ValidationError(errors)

    @classmethod
    def validate_update(cls, instance, attrs):
        errors = {}

        username = attrs.get("username")
        if username:
            cls._capture_errors(errors, cls._validate_username, username)
            if "username" not in errors:
                cls._capture_errors(errors, cls._validate_username_unique, username, instance=instance)

        cls._capture_errors(errors, cls._validate_common_fields, attrs)

        if attrs.get("password"):
            cls._capture_errors(errors, cls._validate_password, attrs.get("password"), attrs, instance=instance)

        if errors:
            raise ValidationError(errors)

    @classmethod
    def _validate_common_fields(cls, attrs):
        errors = {}

        for field in ("first_name", "last_name"):
            if field in attrs:
                cls._capture_errors(errors, cls._validate_person_name, field, attrs.get(field))

        if attrs.get("apellido_materno"):
            cls._capture_errors(errors, cls._validate_person_name, "apellido_materno", attrs.get("apellido_materno"))

        if "telefono" in attrs:
            cls._capture_errors(errors, cls._validate_telefono, attrs.get("telefono"))

        if attrs.get("email"):
            cls._capture_errors(errors, cls._validate_email, attrs.get("email"))

        if errors:
            raise ValidationError(errors)

    @classmethod
    def _validate_username(cls, username):
        try:
            cls.username_validator(username)
        except ValidationError:
            raise ValidationError({
                "username": ["Ingresa un nombre de usuario valido. Usa letras, numeros y @/./+/-/_ solamente."]
            })

    @classmethod
    def _validate_username_unique(cls, username, instance=None):
        queryset = User.objects.filter(username=username)
        if instance is not None:
            queryset = queryset.exclude(pk=instance.pk)
        if queryset.exists():
            raise ValidationError({"username": ["Este nombre de usuario ya existe."]})

    @classmethod
    def _validate_person_name(cls, field, value):
        if value in (None, ""):
            raise ValidationError({field: ["Este campo es obligatorio."]})

        if not cls.name_pattern.fullmatch(value):
            raise ValidationError({
                field: ["Solo se permiten letras y espacios. No uses numeros ni caracteres especiales."]
            })

    @classmethod
    def _validate_telefono(cls, value):
        if value in (None, ""):
            return

        if not str(value).isdigit():
            raise ValidationError({"telefono": ["El telefono debe contener solo numeros."]})

    @classmethod
    def _validate_email(cls, value):
        try:
            validate_email(value)
        except ValidationError:
            raise ValidationError({"email": ["Ingresa un correo electronico valido."]})

    @classmethod
    def _validate_password(cls, password, attrs, instance=None):
        user = instance or User(
            username=attrs.get("username", ""),
            first_name=attrs.get("first_name", ""),
            last_name=attrs.get("last_name", ""),
            apellido_materno=attrs.get("apellido_materno"),
            email=attrs.get("email", ""),
            telefono=attrs.get("telefono"),
            rol=attrs.get("rol"),
        )

        try:
            password_validation.validate_password(password, user=user)
        except ValidationError as exc:
            raise ValidationError({"password": exc.messages})
