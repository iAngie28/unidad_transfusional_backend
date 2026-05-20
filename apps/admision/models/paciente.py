from django.db import models

from core.models import AuditoriaMixin


class Paciente(AuditoriaMixin):
    SEXO_MASCULINO = "M"
    SEXO_FEMENINO = "F"
    EDAD_DIAS = "DIAS"
    EDAD_MESES = "MESES"
    EDAD_ANOS = "ANOS"

    SEXO_CHOICES = [
        (SEXO_MASCULINO, "Masculino"),
        (SEXO_FEMENINO, "Femenino"),
    ]

    EDAD_UNIDAD_CHOICES = [
        (EDAD_DIAS, "Dias"),
        (EDAD_MESES, "Meses"),
        (EDAD_ANOS, "Anos"),
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

    ci = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100, blank=True, null=True)
    edad_valor = models.PositiveSmallIntegerField()
    edad_unidad = models.CharField(max_length=5, choices=EDAD_UNIDAD_CHOICES, default=EDAD_ANOS)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=True, null=True)
    historia_clinica = models.CharField(max_length=50, unique=True)
    grupo_sanguineo = models.CharField(max_length=3, choices=GRUPO_CHOICES)

    class Meta:
        app_label = "admision"
        ordering = ["apellido_paterno", "apellido_materno", "nombre"]
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return f"{self.apellido_paterno} {self.nombre} ({self.ci})"
