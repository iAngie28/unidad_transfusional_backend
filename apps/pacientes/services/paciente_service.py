from ..models.paciente import Paciente
from ..models.grupo_sanguineo import GrupoSanguineo
from django.db import transaction

class PacienteService:
    
    @staticmethod
    @transaction.atomic
    def registrar_grupo_sanguineo(paciente_id, datos_grupo, usuario_str):
        # 1. Desmarcar grupos anteriores como no vigentes
        GrupoSanguineo.objects.filter(paciente_id=paciente_id).update(es_vigente=False)
        
        # 2. Crear el nuevo registro
        nuevo_grupo = GrupoSanguineo.objects.create(
            paciente_id=paciente_id,
            **datos_grupo,
            created_by=usuario_str # Esto vendrá del request.user
        )
        return nuevo_grupo