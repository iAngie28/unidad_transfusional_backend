from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField("Nombre", max_length=150)
    last_name = models.CharField("Apellido paterno", max_length=150)
    apellido_materno = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    rol = models.ForeignKey(
        "users.Rol",
        on_delete=models.PROTECT,
        related_name="usuarios",
        blank=True,
        null=True,
    )

    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        app_label = "users"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        rol = self.rol.nombre if self.rol else "Sin rol"
        return f"{self.username} ({rol})"

    def get_user_permissions(self, obj=None):
        if not self.rol:
            return set()
        return {f"{p.content_type.app_label}.{p.codename}" for p in self.rol.permisos.select_related("content_type")}

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True
        return perm in self.get_user_permissions(obj)

    def has_module_perms(self, app_label):
        if self.is_active and self.is_superuser:
            return True
        if not self.rol:
            return False
        return any(p.content_type.app_label == app_label for p in self.rol.permisos.select_related("content_type"))
