from rest_framework import serializers

from apps.users.models import Rol, User
from apps.users.services import UserValidationService
from core.serializers import BaseModelSerializer


class UserSerializer(BaseModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=False)
    rol = serializers.PrimaryKeyRelatedField(queryset=Rol.objects.all())
    rol_nombre = serializers.CharField(source="rol.nombre", read_only=True)
    rol_descripcion = serializers.CharField(source="rol.descripcion", read_only=True)
    role = serializers.SerializerMethodField()
    role_display = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "apellido_materno",
            "email",
            "telefono",
            "rol",
            "rol_nombre",
            "rol_descripcion",
            "role",
            "role_display",
            "is_active",
            "is_staff",
        ]
        read_only_fields = ["id", "rol_nombre", "rol_descripcion", "role", "role_display"]
        extra_kwargs = {
            "username": {"validators": []},
            "first_name": {"required": True, "allow_blank": False},
            "last_name": {"required": True, "allow_blank": False},
            "email": {"required": False, "allow_blank": True},
        }
        service_class = UserValidationService

    def get_role(self, obj):
        return obj.rol.nombre if obj.rol else None

    def get_role_display(self, obj):
        if not obj.rol:
            return None
        return obj.rol.descripcion or obj.rol.nombre

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
