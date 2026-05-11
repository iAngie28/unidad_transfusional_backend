from django.db import models

from core.models import AuditoriaMixin


class Descarte(AuditoriaMixin):
    ACCION_CHOICES = [
        ("DESCARTE", "Descarte"),
        ("BAJA", "Baja"),
        ("VENCIMIENTO", "Vencimiento"),
    ]

    hemocomponente = models.OneToOneField(
        "inventario.Hemocomponente",
        on_delete=models.PROTECT,
        related_name="descarte",
        db_column="nro_bolsa",
    )
    tipo_accion = models.CharField(max_length=30, choices=ACCION_CHOICES)
    motivo = models.TextField()
    fecha_hora = models.DateTimeField()

    class Meta:
        app_label = "inventario"
        ordering = ["-fecha_hora", "id"]
        verbose_name = "Descarte"
        verbose_name_plural = "Descartes"

    def __str__(self):
        return f"{self.hemocomponente_id} - {self.tipo_accion}"
