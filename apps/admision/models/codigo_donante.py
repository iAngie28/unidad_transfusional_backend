from django.db import models
from core.models import AuditoriaMixin

class CodigoDonante(AuditoriaMixin):
    citacion = models.ForeignKey(
        "admision.CitacionDonante",
        on_delete=models.CASCADE,
        related_name="codigos_donante"
    )
    codigo = models.CharField(max_length=50, unique=True)

    class Meta:
        app_label = "admision"
        ordering = ["codigo"]
        verbose_name = "Codigo de donante"
        verbose_name_plural = "Codigos de donante"

    def __str__(self):
        return f"{self.codigo} - Citacion {self.citacion_id}"
