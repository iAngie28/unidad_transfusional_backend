from django.conf import settings
from django.db import models

from core.models import AuditoriaMixin


class SolicitudTransfusion(AuditoriaMixin):
    HEMOCOMPONENTE_CHOICES = [
        ("SANGRE_TOTAL", "Sangre total"),
        ("GLOBULOS_ROJOS", "Globulos rojos"),
        ("PLASMA", "Plasma"),
        ("PLAQUETAS", "Plaquetas"),
        ("CRIOPRECIPITADO", "Crioprecipitado"),
    ]
    URGENCIA_CHOICES = [
        ("RUTINA", "Rutina"),
        ("URGENTE", "Urgente"),
        ("EMERGENCIA", "Emergencia"),
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

    nro = models.CharField(max_length=30, primary_key=True)
    fecha = models.DateField()
    hora = models.TimeField()
    edad_paciente = models.PositiveSmallIntegerField()
    hto = models.FloatField()
    hb = models.FloatField()
    grupo = models.CharField(max_length=3, choices=GRUPO_CHOICES)
    hemocomponente = models.CharField(max_length=30, choices=HEMOCOMPONENTE_CHOICES)
    cantidad = models.PositiveSmallIntegerField()
    tipo_urgencia = models.CharField(max_length=20, choices=URGENCIA_CHOICES)
    diagnostico = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="solicitudes_recepcionadas",
        db_column="id_user",
    )
    paciente = models.ForeignKey(
        "admision.Paciente",
        on_delete=models.PROTECT,
        related_name="solicitudes_transfusion",
        db_column="id_paciente",
    )
    medico = models.ForeignKey(
        "admision.Medico",
        on_delete=models.PROTECT,
        related_name="solicitudes_transfusion",
        db_column="id_medico",
    )

    class Meta:
        app_label = "admision"
        ordering = ["-fecha", "-hora", "nro"]
        verbose_name = "Solicitud de transfusion"
        verbose_name_plural = "Solicitudes de transfusion"

    def __str__(self):
        return f"Solicitud {self.nro} - {self.paciente_id}"
