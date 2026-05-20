from django.db import models

from core.models import AuditoriaMixin


class Hospital(AuditoriaMixin):
    nombre = models.CharField(max_length=120, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        app_label = "inventario"
        ordering = ["nombre"]
        verbose_name = "Hospital"
        verbose_name_plural = "Hospitales"

    def __str__(self):
        return self.nombre
