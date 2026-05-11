from django.db import models

from core.models import AuditoriaMixin


class Pago(AuditoriaMixin):
    ESTADO_PENDIENTE = "PENDIENTE"
    ESTADO_PAGADO = "PAGADO"
    ESTADO_EXENTO = "EXENTO"
    ESTADO_ANULADO = "ANULADO"

    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, "Pendiente"),
        (ESTADO_PAGADO, "Pagado"),
        (ESTADO_EXENTO, "Exento"),
        (ESTADO_ANULADO, "Anulado"),
    ]

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_PENDIENTE)
    es_sus = models.BooleanField(default=True)
    citacion = models.ForeignKey(
        "admision.CitacionDonante",
        on_delete=models.PROTECT,
        related_name="pagos",
        db_column="id_citacion",
        blank=True,
        null=True,
    )
    transfusion = models.ForeignKey(
        "laboratorio.Transfusion",
        on_delete=models.PROTECT,
        related_name="pagos",
        db_column="id_transfusion",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "admision"
        ordering = ["-created_at", "id"]
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"

    def __str__(self):
        return f"Pago {self.id} - {self.estado}"
