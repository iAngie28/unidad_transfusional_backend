from rest_framework.exceptions import APIException
from rest_framework import status

class BusinessLogicError(APIException):
    """
    Excepción base para errores de lógica de negocio.
    Se traduce automáticamente a un error 400 Bad Request en el Frontend.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Ha ocurrido un error en la lógica del negocio.'
    default_code = 'business_error'

class InsufficientStockError(BusinessLogicError):
    default_detail = 'No hay suficiente stock de este hemocomponente.'
    default_code = 'insufficient_stock'

class IncompatibleBloodError(BusinessLogicError):
    default_detail = 'El grupo sanguíneo no es compatible para esta transfusión.'
    default_code = 'incompatible_blood'