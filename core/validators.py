import re
from django.core.exceptions import ValidationError

class DomainValidators:
    @staticmethod
    def validar_ci(value):
        """Valida que el CI tenga un formato boliviano básico."""
        if not re.match(r'^\d{5,10}(-\d[A-Z])?$', str(value)):
            raise ValidationError("El formato del CI no es válido.")

    @staticmethod
    def validar_grupo_sanguineo(value):
        """Asegura que el grupo sea uno de los 8 estándar."""
        grupos_validos = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        if value not in grupos_validos:
            raise ValidationError(f"{value} no es un grupo sanguíneo válido.")

    @staticmethod
    def validar_edad_paciente(value):
        """Evita registros de edades imposibles."""
        if value < 0 or value > 120:
            raise ValidationError("La edad debe estar entre 0 y 120 años.")