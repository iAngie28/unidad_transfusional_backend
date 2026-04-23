# backend/core/models/bitacora.py
from django.db import models

class Bitacora(models.Model):
    # Cambiamos ForeignKey por CharField o IntegerField para romper el círculo
    usuario_id = models.IntegerField(null=True, blank=True) 
    usuario_email = models.EmailField(null=True, blank=True) # Para saber quién fue sin cruzar tablas
    tabla = models.CharField(max_length=100)
    registro_id = models.CharField(max_length=50)
    accion = models.CharField(max_length=20)
    datos_anteriores = models.JSONField(null=True, blank=True)
    datos_nuevos = models.JSONField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 't_bitacora'