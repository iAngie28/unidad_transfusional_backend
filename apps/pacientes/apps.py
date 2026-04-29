# apps/pacientes/apps.py
from django.apps import AppConfig

class PacientesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.pacientes' # <--- AÑADE EL PREFIX 'apps.'