from django.db import models
from core.models import AuditoriaMixin

class GrupoSanguineo(AuditoriaMixin):
    CELULAR_CHOICES = [('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')]
    FACTOR_CHOICES = [('+', 'Positivo (+)'), ('-', 'Negativo (-)')]

    paciente = models.ForeignKey(
        'pacientes.Paciente', 
        on_delete=models.CASCADE, 
        related_name='historial_grupos'
    )
    grupo_celular = models.CharField(max_length=5, choices=CELULAR_CHOICES)
    factor_rh = models.CharField(max_length=5, choices=FACTOR_CHOICES)
    serologia = models.CharField(max_length=100, blank=True, null=True)
    coombs_directo = models.CharField(max_length=100, blank=True, null=True)
    es_vigente = models.BooleanField(default=True)

    class Meta:
        app_label = 'pacientes'
        ordering = ['-created_at']
        verbose_name = "Grupo Sanguíneo"
        verbose_name_plural = "Grupos Sanguíneos"