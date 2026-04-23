from rest_framework import viewsets, status
from rest_framework.response import Response

class BaseViewSet(viewsets.ModelViewSet):
    """
    Vista genérica que todas las apps usarán.
    """
    service_class = None

    def get_queryset(self):
        return self.service_class.get_all()