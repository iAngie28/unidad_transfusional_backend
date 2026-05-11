from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import IntegrityError

from apps.inventario.models import Descarte
from apps.inventario.serializers import DescarteSerializer
from core.views import AuditoriaViewSetMixin, SearchableQuerySetMixin


class DescarteViewSet(AuditoriaViewSetMixin, SearchableQuerySetMixin, viewsets.ModelViewSet):
    model = Descarte
    serializer_class = DescarteSerializer
    select_related_fields = ("hemocomponente",)
    search_fields = (
        "hemocomponente__nro_bolsa",
        "tipo_accion",
        "motivo",
    )

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {"nro_bolsa": ["Ya existe un registro de descarte para este hemocomponente."]},
                status=status.HTTP_400_BAD_REQUEST
            )
