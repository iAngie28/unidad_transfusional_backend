import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone

from core.models import AuditoriaMixin


class SolicitudTransfusion(AuditoriaMixin):
    EDAD_DIAS = "DIAS"
    EDAD_MESES = "MESES"
    EDAD_ANOS = "ANOS"

    EDAD_UNIDAD_CHOICES = [
        (EDAD_DIAS, "Dias"),
        (EDAD_MESES, "Meses"),
        (EDAD_ANOS, "Anos"),
    ]

    HEMOCOMPONENTE_CHOICES = [
        ("PLASMA_FRESCO_CONGELADO", "Plasma fresco congelado"),
        ("CRIOPRECIPITADOS", "Crioprecipitados"),
        ("CONCENTRADO_PLAQUETAS", "Concentrado de plaquetas"),
        ("PAQUETE_GLOBULAR", "Paquete globular"),
        ("CONCENTRADO_HELITROCITO_PLAQUETAS", "Concentrado de helitrocito y plaquetas por aféresis"),
        ("GLOBULO_ROJO_LAVADO", "Globulo rojo lavado"),
    ]
    URGENCIA_CHOICES = [
        ("URGENTE", "Urgente"),
        ("EN_EL_DIA", "En el dia"),
        ("PROGRAMADA", "Programada"),
    ]
    ESTADO_CHOICES = [
        ("PENDIENTE", "Pendiente"),
        ("FINALIZADA", "Finalizada"),
        ("ARCHIVADA", "Archivada"),
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

    nro = models.CharField(max_length=30, primary_key=True, blank=True)
    fecha = models.DateField()
    hora = models.TimeField()
    edad_valor = models.PositiveSmallIntegerField()
    edad_unidad = models.CharField(max_length=5, choices=EDAD_UNIDAD_CHOICES, default=EDAD_ANOS)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    hto = models.FloatField()
    hb = models.FloatField()
    grupo = models.CharField(max_length=3, choices=GRUPO_CHOICES)
    hemocomponente = models.CharField(max_length=50, choices=HEMOCOMPONENTE_CHOICES)
    cantidad = models.PositiveSmallIntegerField()
    # fraccionado = models.BooleanField(default=False)
    # ml = models.PositiveSmallIntegerField(blank=True, null=True)
    tipo_urgencia = models.CharField(max_length=20, choices=URGENCIA_CHOICES)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default="PENDIENTE")
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
    servicio = models.ForeignKey(
        "admision.Servicio",
        on_delete=models.PROTECT,
        related_name="solicitudes_transfusion",
        db_column="id_servicio",
        null=True,
        blank=True,
    )

    class Meta:
        app_label = "admision"
        ordering = ["-fecha", "-hora", "nro"]
        verbose_name = "Solicitud de transfusion"
        verbose_name_plural = "Solicitudes de transfusion"

    def __str__(self):
        return f"Solicitud {self.nro} - {self.paciente_id}"

    def save(self, *args, **kwargs):
        if not self.nro:
            date_str = timezone.now().strftime("%Y%m%d")
            unique_id = uuid.uuid4().hex[:4].upper()
            self.nro = f"SOL-{date_str}-{unique_id}"
        super().save(*args, **kwargs)
