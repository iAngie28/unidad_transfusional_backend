from django.db import models

from core.models import AuditoriaMixin


class Hemocomponente(AuditoriaMixin):
    TIPO_CHOICES = [
        ("SANGRE_TOTAL", "Sangre total"),
        ("GLOBULOS_ROJOS", "Globulos rojos"),
        ("PLASMA", "Plasma"),
        ("PLAQUETAS", "Plaquetas"),
        ("CRIOPRECIPITADO", "Crioprecipitado"),
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
    ESTADO_CHOICES = [
        ("DISPONIBLE", "Disponible"),
        ("RESERVADO", "Reservado"),
        ("DESPACHADO", "Despachado"),
        ("TRANSFUNDIDO", "Transfundido"),
        ("DESCARTADO", "Descartado"),
        ("VENCIDO", "Vencido"),
    ]

    nro_bolsa = models.CharField(max_length=50, primary_key=True)
    nro_tubuladura = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    grupo_sanguineo = models.CharField(max_length=3, choices=GRUPO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="DISPONIBLE")
    fecha_ingreso = models.DateTimeField()
    fecha_vencimiento = models.DateTimeField()
    devuelto = models.BooleanField(default=False)

    class Meta:
        app_label = "inventario"
        ordering = ["fecha_vencimiento", "nro_bolsa"]
        verbose_name = "Hemocomponente"
        verbose_name_plural = "Hemocomponentes"

    def __str__(self):
        return f"{self.nro_bolsa} - {self.tipo} {self.grupo_sanguineo}"
