from django.db import transaction

from apps.admision.models import Paciente


class PacienteService:
    @staticmethod
    @transaction.atomic
    def registrar_grupo_sanguineo(ci, datos_grupo, usuario=None):
        grupo_sanguineo = datos_grupo.get("grupo_sanguineo")

        if not grupo_sanguineo:
            grupo_celular = datos_grupo.get("grupo_celular")
            factor_rh = datos_grupo.get("factor_rh")
            if grupo_celular and factor_rh:
                grupo_sanguineo = f"{grupo_celular}{factor_rh}"

        if not grupo_sanguineo:
            raise ValueError("Debe enviar grupo_sanguineo o grupo_celular con factor_rh.")

        paciente = Paciente.objects.select_for_update().get(ci=ci)
        paciente.grupo_sanguineo = grupo_sanguineo
        if usuario is not None:
            paciente.created_by = paciente.created_by or usuario
        paciente.save(update_fields=["grupo_sanguineo", "created_by", "updated_at"])
        return paciente
