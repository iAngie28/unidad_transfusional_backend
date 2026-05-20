from django.db import models

from core.models import AuditoriaMixin


class Servicio(AuditoriaMixin):
    nombre = models.CharField(max_length=120, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        app_label = "admision"
        ordering = ["nombre"]
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    def __str__(self):
        return self.nombre
