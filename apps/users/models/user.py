from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    BIOQUIMICO = 'BIOQUIMICO'
    JEFE_UNIDAD = 'JEFE_UNIDAD'
    
    ROLE_CHOICES = [
        (BIOQUIMICO, 'Bioquímico'),
        (JEFE_UNIDAD, 'Jefe de la Unidad Transfusional'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=BIOQUIMICO)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"