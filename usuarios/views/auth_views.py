from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.services.bitacora_service import BitacoraService

class CustomTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # 1. Autenticación estándar (email y password)
        data = super().validate(attrs)
        
        # 2. Obtenemos la Unidad y su Dominio
        # .domains es el related_name que Django-tenants crea automáticamente en el Tenant
        unidad = self.user.unidad
        dominio_principal = unidad.domains.first() if unidad else None
        
        # 3. Expandimos la respuesta para el Frontend
        data['user'] = {
            'email': self.user.email,
            'nombre': f"{self.user.first_name} {self.user.last_name}",
            'rol': self.user.rol.nombre if self.user.rol else None,
            # Estos campos son los que usará React para hacer el "salto" de URL
            'unidad_nombre': unidad.nombre if unidad else "Sin Unidad",
            'subdominio': dominio_principal.domain if dominio_principal else "localhost"
        }

        # 4. Registro en Bitácora (Se guardará en el esquema donde se haga el POST)
        BitacoraService.registrar(
            usuario=self.user,
            instancia=self.user,
            accion='LOGIN',
            nuevos={
                'email': self.user.email, 
                'login_exitoso': True,
                'unidad': unidad.nombre if unidad else 'N/A'
            }
        )
        
        return data

class LoginView(TokenObtainPairView):
    """
    Endpoint central de autenticación.
    """
    serializer_class = CustomTokenSerializer