from core.services.base_service import BaseService
from ..models.usuario import Usuario

class UsuarioService(BaseService):
    model = Usuario

    @classmethod
    def buscar_por_email(cls, email):
        """
        Busca un usuario por su correo electrónico.
        """
        return cls.model.objects.filter(email=email).first()