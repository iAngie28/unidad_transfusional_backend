from django.conf import settings
from django.db import models

from core.models import AuditoriaMixin


class PruebaPretransfusionalPAC(AuditoriaMixin):
    POSITIVO_NEGATIVO_CHOICES = [
        ("POSITIVO", "Positivo"),
        ("NEGATIVO", "Negativo"),
    ]
    GRUPO_CHOICES = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
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
    anti_a = models.CharField(max_length=20, choices=POSITIVO_NEGATIVO_CHOICES)
    anti_b = models.CharField(max_length=20, choices=POSITIVO_NEGATIVO_CHOICES)
    anti_ab = models.CharField(max_length=20, choices=POSITIVO_NEGATIVO_CHOICES)
    anti_d = models.CharField(max_length=20, choices=POSITIVO_NEGATIVO_CHOICES)
    control_rhesus = models.CharField(max_length=20, choices=POSITIVO_NEGATIVO_CHOICES)
    alfa = models.CharField(max_length=20, choices=POSITIVO_NEGATIVO_CHOICES)
    beta = models.CharField(max_length=20, choices=POSITIVO_NEGATIVO_CHOICES)
    o = models.CharField(max_length=20, choices=POSITIVO_NEGATIVO_CHOICES)
    fenotipo = models.CharField(max_length=3, choices=GRUPO_CHOICES)
    hto = models.FloatField()
    hb = models.FloatField()
    coombs_directo = models.CharField(max_length=20, choices=POSITIVO_NEGATIVO_CHOICES)
    resultado = models.CharField(max_length=100)

    class Meta:
        app_label = "laboratorio"
        ordering = ["-fecha_hora", "id"]
        verbose_name = "Prueba pretransfusional PAC"
        verbose_name_plural = "Pruebas pretransfusionales PAC"

    def __str__(self):
        return f"PAC {self.id} - {self.paciente_id}"
