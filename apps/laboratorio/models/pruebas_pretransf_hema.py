from django.conf import settings
from django.db import models

from core.models import AuditoriaMixin


class PruebasPretransfHema(AuditoriaMixin):
    RESULTADO_CHOICES = [
        ("POSITIVO", "Positivo"),
        ("NEGATIVO", "Negativo"),
        ("NO_REALIZADO", "No realizado"),
    ]

    fecha = models.DateTimeField()
    salina = models.CharField(max_length=100)
    albumina = models.CharField(max_length=100)
    liss = models.CharField(max_length=100)
    coombs = models.CharField(max_length=100)
    cruzada_mayor = models.CharField(max_length=100)
    cruzada_menor = models.CharField(max_length=100)
    hemolisis = models.CharField(max_length=100)
    anti_a = models.CharField(max_length=20, choices=RESULTADO_CHOICES)
    anti_b = models.CharField(max_length=20, choices=RESULTADO_CHOICES)
    anti_ab = models.CharField(max_length=20, choices=RESULTADO_CHOICES)
    anti_d = models.CharField(max_length=20, choices=RESULTADO_CHOICES)
    celula_a = models.CharField(max_length=100)
    celula_b = models.CharField(max_length=100)
    celula_o = models.CharField(max_length=100)
    fenotipo = models.CharField(max_length=100)
    hemocomponente = models.ForeignKey(
        "inventario.Hemocomponente",
        on_delete=models.PROTECT,
        related_name="pruebas_pretransf_hema",
        db_column="nro_bolsa",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="pruebas_pretransf_hema",
        db_column="user_id",
    )
    solicitud = models.ForeignKey(
        "admision.SolicitudTransfusion",
        on_delete=models.PROTECT,
        related_name="pruebas_pretransf_hema",
        db_column="nro_solicitud",
    )

    class Meta:
        app_label = "laboratorio"
        ordering = ["-fecha", "id"]
        verbose_name = "Prueba pretransfusional hema"
        verbose_name_plural = "Pruebas pretransfusionales hema"

    def __str__(self):
        return f"Hema {self.id} - {self.hemocomponente_id}"
