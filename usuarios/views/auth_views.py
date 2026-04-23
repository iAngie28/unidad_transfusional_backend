from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from core.services.bitacora_service import BitacoraService
from ..serializers.registro_serializer import RegistroSerializer

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


class RegistroView(generics.CreateAPIView):
    """
    Endpoint público para registrar una nueva Unidad Transfusional con su usuario administrador.
    
    Acepta:
    - first_name: Nombre del administrador
    - last_name: Apellido del administrador
    - email: Email único del administrador
    - password: Contraseña (min 8 caracteres)
    - nombre: Nombre de la Unidad Transfusional
    - subdominio: (Opcional) Subdominio. Si no se proporciona, se genera del nombre
    
    Retorna:
    - access: Token JWT de acceso
    - refresh: Token JWT de refresco
    - subdominio: El subdominio creado (generado o proporcionado)
    - unidad: Información de la unidad creada
    """
    serializer_class = RegistroSerializer
    permission_classes = [AllowAny]  # Permite el acceso
    authentication_classes = []
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Crear la unidad, usuario y retornar tokens
        result = serializer.save()
        
        return Response(
            {
                'access': result['access'],
                'refresh': result['refresh'],
                'user': {
                    'email': request.data.get('email'),
                    'nombre': f"{request.data.get('first_name')} {request.data.get('last_name')}",
                    'subdominio': result['subdominio'],
                    'unidad_nombre': result['unidad']['nombre'],
                },
            },
            status=status.HTTP_201_CREATED
        )