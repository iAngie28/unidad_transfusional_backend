from django.db import models
from django_tenants.models import TenantMixin

class UnidadTransfusional(TenantMixin):
    nombre = models.CharField(max_length=100)
    nivel_complejidad = models.CharField(max_length=50, blank=True, null=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    
    # Crea el esquema automáticamente al guardar
    auto_create_schema = True

    def __str__(self):
        return self.nombre