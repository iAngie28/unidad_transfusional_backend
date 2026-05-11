from django.conf import settings
from django.db import models

from core.models import AuditoriaMixin


class CitacionDonante(AuditoriaMixin):
    solicitud = models.ForeignKey(
        "admision.SolicitudTransfusion",
        on_delete=models.CASCADE,
        related_name="citaciones_donante",
        db_column="nro_solicitud",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="citaciones_donante_recepcionadas",
        db_column="id_user",
    )
    fecha = models.DateField()
    servicio = models.CharField(max_length=120)
    sala_cama = models.CharField(max_length=60, blank=True, null=True)
    cantidad = models.PositiveSmallIntegerField()
    codigo_donante = models.CharField(max_length=50, unique=True)
    hora = models.TimeField()
    grupo_factor = models.CharField(max_length=5)
    tipo = models.CharField(max_length=100)

    class Meta:
        app_label = "admision"
        ordering = ["-fecha", "-hora", "codigo_donante"]
        verbose_name = "Citacion de donante"
        verbose_name_plural = "Citaciones de donantes"

    def __str__(self):
        return f"Citacion {self.codigo_donante} - {self.solicitud_id}"
