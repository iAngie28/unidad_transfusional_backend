from rest_framework import viewsets

from apps.laboratorio.models import Transfusion
from apps.laboratorio.serializers import TransfusionSerializer
from core.views import AuditoriaViewSetMixin, SearchableQuerySetMixin


class TransfusionViewSet(AuditoriaViewSetMixin, SearchableQuerySetMixin, viewsets.ModelViewSet):
    model = Transfusion
    serializer_class = TransfusionSerializer
    select_related_fields = ("hemocomponente", "paciente", "user", "servicio")
    search_fields = (
        "hemocomponente__nro_bolsa",
        "paciente__ci",
        "paciente__nombre",
        "paciente__apellido_paterno",
        "user__username",
        "servicio__nombre",
        "diagnostico",
        "grupo_cabecera_h",
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        
        paciente = self.request.query_params.get("paciente")
        hemocomponente = self.request.query_params.get("hemocomponente")
        solicitud = self.request.query_params.get("solicitud")
        
        if paciente:
            queryset = queryset.filter(paciente_id=paciente)
        if hemocomponente:
            queryset = queryset.filter(hemocomponente_id=hemocomponente)
        if solicitud:
            from apps.laboratorio.models import PruebasPretransfHema
            pruebas = PruebasPretransfHema.objects.filter(solicitud_id=solicitud)
            hemocomponentes_ids = pruebas.values_list("hemocomponente_id", flat=True)
            queryset = queryset.filter(hemocomponente_id__in=hemocomponentes_ids)
            
        return queryset

    def perform_create(self, serializer):
        transfusion = serializer.save()
        
        # Find the related PruebasPretransfHema to get the original Solicitud
        from apps.laboratorio.models import PruebasPretransfHema
        prueba = PruebasPretransfHema.objects.filter(hemocomponente=transfusion.hemocomponente).first()
        if prueba and prueba.solicitud:
            solicitud = prueba.solicitud
            if solicitud.estado != "FINALIZADA":
                solicitud.estado = "FINALIZADA"
                solicitud.save(update_fields=["estado"])

