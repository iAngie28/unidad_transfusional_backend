# usuarios/models/usuario.py
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from .rol import Rol

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    # Relación para saber de qué Unidad es el usuario
    unidad = models.ForeignKey(
        'core.UnidadTransfusional', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='usuarios'
    )
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, null=True)
    esta_activo = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    groups = models.ManyToManyField(
        Group,
        related_name="usuario_custom_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="usuario_custom_set",
        blank=True
    )

    def __str__(self):
        return f"{self.email} - {self.unidad.nombre if self.unidad else 'Sin Unidad'}"