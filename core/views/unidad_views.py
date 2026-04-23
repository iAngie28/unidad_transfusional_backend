from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import UnidadTransfusional

class UnidadInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # El middleware ya se encargó de filtrar la unidad por el subdominio
        unidad = request.tenant 
        return Response({
            'nombre': unidad.nombre,
            'nivel': unidad.nivel_complejidad,
            'schema': unidad.schema_name
        })