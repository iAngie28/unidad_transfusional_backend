from rest_framework import serializers
from ..models import Usuario, Rol

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre', 'descripcion']

class UsuarioSerializer(serializers.ModelSerializer):
    rol_detalle = RolSerializer(source='rol', read_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'email', 'first_name', 'last_name', 'rol', 'rol_detalle', 'esta_activo']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Lógica para encriptar password al crear usuarios
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance