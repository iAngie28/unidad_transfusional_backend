from django.conf import settings
from django.db import models

from core.models import AuditoriaMixin


class Transfusion(AuditoriaMixin):
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

    servicio = models.ForeignKey(
        "admision.Servicio",
        on_delete=models.PROTECT,
        related_name="transfusiones",
        db_column="id_servicio",
    )
    diagnostico = models.TextField()
    ate_trans_alerg = models.BooleanField(default=False)
    grupo_cabecera_h = models.CharField(max_length=3, choices=GRUPO_CHOICES)
    hora_inicio = models.DateTimeField()
    hora_fin = models.DateTimeField(blank=True, null=True)
    fraccionado = models.BooleanField(default=False)
    ml = models.PositiveSmallIntegerField(default=1000)
    hemocomponente = models.ForeignKey(
        "inventario.Hemocomponente",
        on_delete=models.PROTECT,
        related_name="transfusiones",
        db_column="nro_bolsa",
    )
    paciente = models.ForeignKey(
        "admision.Paciente",
        on_delete=models.PROTECT,
        related_name="transfusiones",
        db_column="ci_paciente",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="transfusiones_responsable",
        db_column="user_id",
    )

    class Meta:
        app_label = "laboratorio"
        ordering = ["-hora_inicio", "id"]
        verbose_name = "Transfusion"
        verbose_name_plural = "Transfusiones"

    def __str__(self):
        return f"Transfusion {self.id} - {self.paciente_id}"
