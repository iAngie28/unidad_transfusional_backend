from django.utils import timezone

from rest_framework import viewsets

from apps.inventario.models import Hemocomponente, Trazabilidad
from apps.inventario.serializers import HemocomponenteSerializer
from core.views import AuditoriaViewSetMixin, SearchableQuerySetMixin

# Mapeo de estado del hemocomponente → evento de trazabilidad
ESTADO_A_EVENTO = {
    "RESERVADO": "RESERVA",
    "DESPACHADO": "DESPACHO",
    "DISPONIBLE": "DEVOLUCION",
    "DESCARTADO": "DESCARTE",
    "VENCIDO": "DESCARTE",
    # TRANSFUNDIDO se registra a través del flujo de transfusión, no aquí
}


class HemocomponenteViewSet(AuditoriaViewSetMixin, SearchableQuerySetMixin, viewsets.ModelViewSet):
    model = Hemocomponente
    serializer_class = HemocomponenteSerializer
    search_fields = (
        "nro_bolsa",
        "nro_tubuladura",
        "tipo",
        "grupo_sanguineo",
        "estado",
    )

    def perform_update(self, serializer):
        instance = self.get_object()
        estado_anterior = instance.estado
        updated = serializer.save()

        # Si el estado cambió, registrar el evento de trazabilidad correspondiente
        nuevo_estado = updated.estado
        if nuevo_estado != estado_anterior:
            evento = ESTADO_A_EVENTO.get(nuevo_estado)
            if evento:
                Trazabilidad.objects.create(
                    hemocomponente=updated,
                    evento=evento,
                    encargado=self.request.user,
                    fecha_hora=timezone.now(),
                    created_by=self.request.user,
                )
