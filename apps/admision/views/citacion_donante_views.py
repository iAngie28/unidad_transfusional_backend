from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import ProtectedError

from apps.admision.models import CitacionDonante
from apps.admision.serializers import CitacionDonanteSerializer
from core.views import AuditoriaViewSetMixin, SearchableQuerySetMixin


class CitacionDonanteViewSet(AuditoriaViewSetMixin, SearchableQuerySetMixin, viewsets.ModelViewSet):
    model = CitacionDonante
    serializer_class = CitacionDonanteSerializer
    select_related_fields = ("solicitud", "user")
    search_fields = (
        "solicitud__nro",
        "codigo_donante",
        "servicio",
        "grupo_factor",
        "tipo",
    )

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"error": "No se puede eliminar esta citación porque tiene pagos u otros registros asociados."},
                status=status.HTTP_400_BAD_REQUEST
            )

