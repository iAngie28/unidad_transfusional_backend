from django.db import models

from core.models import AuditoriaMixin


class ConsentimientoInformado(AuditoriaMixin):
    solicitud = models.ForeignKey(
        "admision.SolicitudTransfusion",
        on_delete=models.CASCADE,
        related_name="consentimientos",
        db_column="nro_solicitud",
    )
    fecha = models.DateField()
    servicio = models.CharField(max_length=120)
    nombre_familiar = models.CharField(max_length=100)
    apellido_paterno_familiar = models.CharField(max_length=100)
    apellido_materno_familiar = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=30)
    ci = models.CharField(max_length=20)

    class Meta:
        app_label = "admision"
        ordering = ["-fecha", "solicitud"]
        verbose_name = "Consentimiento informado"
        verbose_name_plural = "Consentimientos informados"

    def __str__(self):
        return f"Consentimiento {self.solicitud_id} - {self.ci}"
