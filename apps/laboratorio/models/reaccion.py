from django.db import models

from core.models import AuditoriaMixin


class Reaccion(AuditoriaMixin):
    transfusion = models.ForeignKey(
        "laboratorio.Transfusion",
        on_delete=models.CASCADE,
        related_name="reacciones",
        db_column="id_transfusion",
    )
    descripcion = models.TextField()
    fecha_hora = models.DateTimeField()

    class Meta:
        app_label = "laboratorio"
        ordering = ["-fecha_hora", "id"]
        verbose_name = "Reaccion"
        verbose_name_plural = "Reacciones"

    def __str__(self):
        return f"Reaccion {self.id} - Transfusion {self.transfusion_id}"
