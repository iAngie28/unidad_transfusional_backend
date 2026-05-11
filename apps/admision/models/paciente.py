from django.db import models

from core.models import AuditoriaMixin


class Paciente(AuditoriaMixin):
    SEXO_MASCULINO = "M"
    SEXO_FEMENINO = "F"
    SEXO_OTRO = "O"

    SEXO_CHOICES = [
        (SEXO_MASCULINO, "Masculino"),
        (SEXO_FEMENINO, "Femenino"),
        (SEXO_OTRO, "Otro"),
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
    edad = models.PositiveSmallIntegerField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    historia_clinica = models.CharField(max_length=50, unique=True)
    grupo_sanguineo = models.CharField(max_length=3, choices=GRUPO_CHOICES)

    class Meta:
        app_label = "admision"
        ordering = ["apellido_paterno", "apellido_materno", "nombre"]
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return f"{self.apellido_paterno} {self.nombre} ({self.ci})"
