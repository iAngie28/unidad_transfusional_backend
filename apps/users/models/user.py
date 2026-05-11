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
