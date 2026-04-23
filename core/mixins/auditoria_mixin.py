from django.forms.models import model_to_dict
from ..services.bitacora_service import BitacoraService

class AuditoriaMixin:
    def perform_create(self, serializer):
        instance = serializer.save()
        # Registramos en la bitácora
        BitacoraService.registrar(
            usuario=self.request.user,
            instancia=instance,
            accion='CREAR',
            nuevos=model_to_dict(instance)
        )

    def perform_update(self, serializer):
        # 1. Capturamos el estado actual antes de guardar
        old_instance = self.get_object()
        datos_anteriores = model_to_dict(old_instance)
        
        # 2. Guardamos los cambios
        instance = serializer.save()
        
        # 3. Registramos el cambio
        BitacoraService.registrar(
            usuario=self.request.user,
            instancia=instance,
            accion='ACTUALIZAR',
            anteriores=datos_anteriores,
            nuevos=model_to_dict(instance)
        )

    def perform_destroy(self, instance):
        datos_anteriores = model_to_dict(instance)
        registro_id = instance.pk
        tabla = instance._meta.db_table
        
        instance.delete()
        
        BitacoraService.registrar(
            usuario=self.request.user,
            instancia=instance, # Pasamos la instancia aunque esté borrada para metadatos
            accion='ELIMINAR',
            anteriores=datos_anteriores
        )