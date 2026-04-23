from django.db import models

class Rol(models.Model):
    BIOQUIMICO = 'BIO'
    JEFE_UNIDAD = 'JEF'
    ADMIN_SISTEMA = 'ADM'
    
    ROLES_CHOICES = [
        (BIOQUIMICO, 'Bioquímico'),
        (JEFE_UNIDAD, 'Jefe de Unidad'),
        (ADMIN_SISTEMA, 'Administrador del Sistema'),
    ]

    nombre = models.CharField(max_length=3, choices=ROLES_CHOICES, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.get_nombre_display()