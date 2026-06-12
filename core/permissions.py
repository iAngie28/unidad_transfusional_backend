from rest_framework import permissions

class RoleBasedPermission(permissions.BasePermission):
    """
    Permiso dinámico que verifica si el usuario tiene el permiso de Django
    requerido para la acción específica en el modelo consultado.
    """

    def has_permission(self, request, view):
        # Si el usuario no está autenticado, no tiene acceso
        if not request.user or not request.user.is_authenticated:
            return False
            
        # Si la vista no define el modelo, no podemos validar a este nivel
        model = getattr(view, 'model', None)
        if not model:
            # Intentar obtener el modelo del queryset
            if hasattr(view, 'get_queryset'):
                model = view.get_queryset().model
                
        if not model:
            return True # O podríamos devolver False y ser restrictivos

        app_label = model._meta.app_label
        model_name = model._meta.model_name
        
        # Mapear los métodos HTTP a las acciones por defecto de Django
        action_mapping = {
            'GET': 'view',
            'OPTIONS': 'view',
            'HEAD': 'view',
            'POST': 'add',
            'PUT': 'change',
            'PATCH': 'change',
            'DELETE': 'delete'
        }
        
        action = action_mapping.get(request.method)
        if not action:
            return False
            
        # Nombre del permiso esperado (ej. "users.view_user")
        permission_codename = f"{app_label}.{action}_{model_name}"
        
        return request.user.has_perm(permission_codename)
