from rest_framework import serializers

class BaseModelSerializer(serializers.ModelSerializer):
    """
    Serializador base del que heredarán todos los modelos del sistema.
    Aquí puedes agregar lógica global en el futuro.
    """
    # Ejemplo de algo global: podrías formatear fechas o estandarizar errores aquí
    pass