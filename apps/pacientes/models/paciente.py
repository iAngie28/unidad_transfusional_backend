from django.db import models
from core.models import AuditoriaMixin

class Paciente(AuditoriaMixin):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    historia_clinica = models.CharField(max_length=50, unique=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'pacientes'
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"