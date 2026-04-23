from rest_framework import serializers
from django.db import transaction
from django_tenants.utils import schema_context
import re
from core.models import UnidadTransfusional, Dominio
from ..models import Usuario, Rol
from django.conf import settings

def normalizar_subdominio(texto):
    """
    Convierte el texto en un subdominio válido:
    - Minúsculas
    - Reemplaza espacios y caracteres especiales con guiones
    - Solo permite caracteres alfanuméricos y guiones
    """
    if not texto:
        return ""
    
    # Convertir a minúsculas
    texto = texto.lower()
    
    # Reemplazar espacios y caracteres especiales con guiones
    texto = re.sub(r'[^a-z0-9\-]', '-', texto)
    
    # Reemplazar múltiples guiones consecutivos con un único guión
    texto = re.sub(r'-+', '-', texto)
    
    # Remover guiones al inicio y final
    texto = texto.strip('-')
    
    return texto


class RegistroSerializer(serializers.Serializer):
    """
    Serializer para el registro de una nueva Unidad con su administrador.
    
    Este endpoint es público y crea:
    - Una nueva UnidadTransfusional
    - Un nuevo Dominio asociado
    - Un Usuario administrador
    """
    
    # Datos del Usuario Administrador
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    
    # Datos de la Unidad
    nombre = serializers.CharField(max_length=100, required=True)
    subdominio = serializers.CharField(max_length=100, required=False, allow_blank=True)
    
    def validate_email(self, value):
        """Validar que el email no exista en el esquema público."""
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado.")
        return value
    
    def validate_subdominio(self, value):
        """
        Validar que el subdominio sea único y válido.
        Si está vacío, se generará automáticamente del nombre de la unidad.
        """
        if not value:
            # Se generará en validate()
            return value
        
        # Normalizar el subdominio
        value = normalizar_subdominio(value)
        
        # Validar que no exista una unidad con este subdominio
        if UnidadTransfusional.objects.filter(schema_name=value).exists():
            raise serializers.ValidationError(f"El subdominio '{value}' ya está en uso.")
        
        return value
    
    def validate(self, data):
        """
        Validar los datos completos y generar subdominio si no se proporciona.
        """
        nombre_unidad = data.get('nombre', '')
        subdominio = data.get('subdominio', '')
        
        # Si no hay subdominio, generarlo del nombre de la unidad
        if not subdominio:
            subdominio = normalizar_subdominio(nombre_unidad)
            if not subdominio:
                raise serializers.ValidationError("No se pudo generar un subdominio válido del nombre de la unidad.")
            data['subdominio'] = subdominio
        
        # Validar que el subdominio sea único
        if UnidadTransfusional.objects.filter(schema_name=data['subdominio']).exists():
            raise serializers.ValidationError(f"El subdominio '{data['subdominio']}' ya está en uso.")
        
        return data
    
    @transaction.atomic
    def create(self, validated_data):
        """
        Crear la Unidad, Dominio y Usuario en una transacción atómica.
        
        Retorna un diccionario con los tokens JWT y el subdominio.
        """
        # Extraer datos
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        password = validated_data['password']
        nombre_unidad = validated_data['nombre']
        subdominio = validated_data['subdominio']
        
        # 1. Crear la Unidad Transfusional (dispara creación del esquema)
        # 1. Crear la Unidad Transfusional
        unidad = UnidadTransfusional.objects.create(
            schema_name=subdominio,  # Requerido por la librería
            nombre=nombre_unidad     # Requerido por TU modelo
        )
        # 2. Definir el dominio base según el entorno
        # settings.DEBUG es True en tu PC y False en Render
        base_domain = "localhost" if settings.DEBUG else "tu-app.onrender.com"
        full_domain = f"{subdominio}.{base_domain}"

        # Crear el Dominio asociado
        dominio = Dominio.objects.create(
            domain=full_domain,
            tenant=unidad,
            is_primary=True
        )
        
        # 3. Crear el Usuario en el esquema público (no en el tenant)
        # El usuario pertenecerá a la unidad y podrá tener rol de administrador
        usuario = Usuario.objects.create_user(
            email=email,
            username=email,  # usar email como username
            first_name=first_name,
            last_name=last_name,
            password=password,
            unidad=unidad,
            is_active=True,     # <--- Asegura el estándar de Django
            esta_activo=True
        )
        
        # 4. Asignarle el rol de Jefe de Unidad como administrador
        try:
            rol_jefe = Rol.objects.get(nombre=Rol.JEFE_UNIDAD)
            usuario.rol = rol_jefe
            usuario.save()
        except Rol.DoesNotExist:
            # Si no existe, al menos queda sin rol pero funcional
            pass
        
        # 5. Generar tokens JWT
        from rest_framework_simplejwt.tokens import RefreshToken
        
        refresh = RefreshToken.for_user(usuario)
        
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'subdominio': subdominio,
            'unidad': {
                'nombre': nombre_unidad,
                'dominio': f"{subdominio}.localhost"
            }
        }
    
    def save(self, **kwargs):
        """No se llama directamente, se usa create()."""
        return self.create(self.validated_data)
