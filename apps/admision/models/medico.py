from django.db import models

from core.models import AuditoriaMixin


class Medico(AuditoriaMixin):
    especialidad = models.ForeignKey(
        "admision.Especialidad",
        on_delete=models.PROTECT,
        related_name="medicos",
        db_column="id_especialidad",
    )
    matricula_profesional = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        app_label = "admision"
        ordering = ["apellido_paterno", "apellido_materno", "nombre"]
        verbose_name = "Medico"
        verbose_name_plural = "Medicos"

    def __str__(self):
        return f"{self.apellido_paterno} {self.nombre} - {self.matricula_profesional}"
