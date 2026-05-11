from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    """
    Nota de Arquitecto: 
    Como el Login NO guarda ni actualiza un modelo directamente (solo valida datos), 
    está perfecto que herede del Serializer normal de DRF.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
