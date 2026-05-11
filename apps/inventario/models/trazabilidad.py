from django.conf import settings
from django.db import models

from core.models import AuditoriaMixin


class Trazabilidad(AuditoriaMixin):
    EVENTO_CHOICES = [
        ("INGRESO", "Ingreso"),
        ("FRACCIONAMIENTO", "Fraccionamiento"),
        ("RESERVA", "Reserva"),
        ("DESPACHO", "Despacho"),
        ("DEVOLUCION", "Devolucion"),
        ("DESCARTE", "Descarte"),
    ]

    hemocomponente = models.ForeignKey(
        "inventario.Hemocomponente",
        on_delete=models.CASCADE,
        related_name="trazabilidades",
        db_column="nro_bolsa",
    )
    evento = models.CharField(max_length=30, choices=EVENTO_CHOICES)
    encargado = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="trazabilidades_registradas",
    )
    fecha_hora = models.DateTimeField()

    class Meta:
        app_label = "inventario"
        ordering = ["-fecha_hora", "id"]
        verbose_name = "Trazabilidad"
        verbose_name_plural = "Trazabilidades"

    def __str__(self):
        return f"{self.hemocomponente_id} - {self.evento}"
