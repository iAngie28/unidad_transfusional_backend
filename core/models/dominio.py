from django.db import models
from django_tenants.models import DomainMixin

class Dominio(DomainMixin):
    pass
    # DomainMixin ya incluye los campos 'domain' y 'tenant' (FK)
    
    def __str__(self):
        return self.domain
    