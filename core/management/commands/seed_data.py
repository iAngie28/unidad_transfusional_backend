from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.pacientes.models import Paciente
from apps.pacientes.services.paciente_service import PacienteService
import datetime

User = get_user_model()

class Command(BaseCommand):
    help = 'Carga datos iniciales de prueba para la Unidad Transfusional'

    def handle(self, *args, **kwargs):
        self.stdout.write('Iniciando carga de datos...')

        # 1. CREAR USUARIOS
        self.stdout.write('- Creando usuarios...')
        bio, _ = User.objects.get_or_create(
            username='bio01',
            defaults={
                'first_name': 'Juan',
                'last_name': 'Bioquimico',
                'role': 'BIOQUIMICO',
                'is_staff': True
            }
        )
        bio.set_password('password123')
        bio.save()

        jefe, _ = User.objects.get_or_create(
            username='jefe01',
            defaults={
                'first_name': 'Dra. Ana',
                'last_name': 'Jefa',
                'role': 'JEFE_UNIDAD',
                'is_staff': True
            }
        )
        jefe.set_password('password123')
        jefe.save()

        # 2. CREAR PACIENTES (Usando el Service para respetar lógica)
        self.stdout.write('- Creando pacientes y grupos...')
        pacientes_data = [
            {'nombre': 'Carlos', 'apellido': 'Gomez', 'dni': '12345678', 'hc': 'HC-001', 'grupo': 'A', 'factor': '+'},
            {'nombre': 'Maria', 'apellido': 'Rodriguez', 'dni': '87654321', 'hc': 'HC-002', 'grupo': 'O', 'factor': '-'},
        ]

        for p in pacientes_data:
            paciente, created = Paciente.objects.get_or_create(
                dni=p['dni'],
                defaults={
                    'nombre': p['nombre'],
                    'apellido': p['apellido'],
                    'historia_clinica': p['hc'],
                    'fecha_nacimiento': datetime.date(1990, 5, 20),
                    'created_by': bio
                }
            )
            if created:
                # Usamos el Service para registrar el grupo y que maneje la "Vigencia"
                PacienteService.registrar_grupo_sanguineo(
                    paciente.id, 
                    {'grupo_celular': p['grupo'], 'factor_rh': p['factor']}, 
                    bio
                )

        self.stdout.write(self.style.SUCCESS('Seeder ejecutado con éxito.'))