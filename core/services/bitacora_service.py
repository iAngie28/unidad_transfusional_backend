# backend/core/services/bitacora_service.py
from ..models.bitacora import Bitacora

class BitacoraService:
    @staticmethod
    def registrar(usuario, instancia, accion, anteriores=None, nuevos=None):
        # El error estaba aquí: intentabas usar 'nuevos' en lugar de 'datos_nuevos'
        Bitacora.objects.create(
            usuario_id=usuario.id if usuario and usuario.is_authenticated else None,
            usuario_email=usuario.email if usuario and usuario.is_authenticated else "sistema",
            tabla=instancia._meta.db_table,
            registro_id=str(instancia.pk),
            accion=accion,
            datos_anteriores=anteriores, # Mapeo correcto
            datos_nuevos=nuevos           # <--- CORRECCIÓN AQUÍ (debe ser datos_nuevos)
        )