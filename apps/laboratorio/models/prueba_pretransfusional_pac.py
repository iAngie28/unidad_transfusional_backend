from django.conf import settings
from django.db import models

from core.models import AuditoriaMixin


class PruebaPretransfusionalPAC(AuditoriaMixin):
    REACTIVO_CHOICES = [
        ("POSITIVO", "Positivo"),
        ("NEGATIVO", "Negativo"),
        ("NO_REALIZADO", "No realizado"),
    ]
    RESULTADO_CHOICES = [
        ("APTO", "Apto"),
        ("NO_APTO", "No apto"),
        ("PENDIENTE", "Pendiente"),
    ]

    fecha_hora = models.DateTimeField()
    paciente = models.ForeignKey(
        "admision.Paciente",
        on_delete=models.PROTECT,
        related_name="pruebas_pretransfusionales_pac",
        db_column="paciente_id",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="pruebas_pretransfusionales_pac",
        db_column="user_id",
    )
    solicitud = models.ForeignKey(
        "admision.SolicitudTransfusion",
        on_delete=models.PROTECT,
        related_name="pruebas_pretransfusionales_pac",
        db_column="nro_solicitud",
    )
    anti_a = models.CharField(max_length=20, choices=REACTIVO_CHOICES)
    anti_b = models.CharField(max_length=20, choices=REACTIVO_CHOICES)
    anti_ab = models.CharField(max_length=20, choices=REACTIVO_CHOICES)
    anti_d = models.CharField(max_length=20, choices=REACTIVO_CHOICES)
    control_rhesus = models.CharField(max_length=100)
    alfa = models.CharField(max_length=100)
    beta = models.CharField(max_length=100)
    o = models.CharField(max_length=100)
    fenotipo = models.CharField(max_length=100)
    hto = models.FloatField()
    hb = models.FloatField()
    coombs_directo = models.CharField(max_length=100)
    resultado = models.CharField(max_length=20, choices=RESULTADO_CHOICES)

    class Meta:
        app_label = "laboratorio"
        ordering = ["-fecha_hora", "id"]
        verbose_name = "Prueba pretransfusional PAC"
        verbose_name_plural = "Pruebas pretransfusionales PAC"

    def __str__(self):
        return f"PAC {self.id} - {self.paciente_id}"
