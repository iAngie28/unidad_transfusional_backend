from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from apps.users.models import Rol, User


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "descripcion")
    search_fields = ("nombre", "descripcion")
    filter_horizontal = ("permisos",)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "apellido_materno",
        "telefono",
        "rol",
        "is_active",
        "is_staff",
    )
    list_filter = ("rol", "is_active", "is_staff", "is_superuser")
    search_fields = ("username", "first_name", "last_name", "apellido_materno", "telefono")
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Datos del personal", {"fields": ("apellido_materno", "telefono", "rol")}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        (
            "Datos del personal",
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "apellido_materno",
                    "telefono",
                    "rol",
                    "email",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
