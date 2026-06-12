from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.admision.models import SolicitudTransfusion
from apps.admision.serializers import SolicitudTransfusionSerializer
from core.views import AuditoriaViewSetMixin, SearchableQuerySetMixin


class SolicitudTransfusionViewSet(AuditoriaViewSetMixin, SearchableQuerySetMixin, viewsets.ModelViewSet):
    model = SolicitudTransfusion
    serializer_class = SolicitudTransfusionSerializer
    select_related_fields = ("user", "paciente", "medico")
    search_fields = (
        "nro",
        "paciente__ci",
        "paciente__nombre",
        "paciente__apellido_paterno",
        "medico__nombre",
        "medico__apellido_paterno",
        "diagnostico",
        "hemocomponente",
        "tipo_urgencia",
    )
    def get_queryset(self):
        queryset = super().get_queryset()
        
        paciente = self.request.query_params.get("paciente")
        estado = self.request.query_params.get("estado")
        
        if paciente:
            queryset = queryset.filter(paciente_id=paciente)
        if estado:
            queryset = queryset.filter(estado=estado)
            
        return queryset

    @action(detail=True, methods=["patch"])
    def archivar(self, request, pk=None):
        solicitud = self.get_object()
        if solicitud.estado != "PENDIENTE":
            return Response({"detail": "Solo las solicitudes pendientes pueden ser archivadas."}, status=400)
        solicitud.estado = "ARCHIVADA"
        solicitud.save()
        return Response({"status": "Solicitud archivada con éxito."})
