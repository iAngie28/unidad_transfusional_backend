from rest_framework import serializers
from core.serializers import BaseModelSerializer 
from apps.users.models.user import User

class UserSerializer(BaseModelSerializer): 
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'role_display']

class LoginSerializer(serializers.Serializer):
    """
    Nota de Arquitecto: 
    Como el Login NO guarda ni actualiza un modelo directamente (solo valida datos), 
    está perfecto que herede del Serializer normal de DRF.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)