from django.contrib.auth.models import Permission
from django.db import models


class Rol(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    permisos = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="roles_personalizados",
    )

    class Meta:
        app_label = "users"
        ordering = ["nombre"]
        verbose_name = "Rol"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.nombre
