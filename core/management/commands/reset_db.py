from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from django.conf import settings

class Command(BaseCommand):
    help = 'Limpia la base de datos, genera migraciones y las aplica.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('--- INICIANDO RESET DE BASE DE DATOS ---'))
        
        # 1. Limpiar esquema (Solo si es Postgres)
        with connection.cursor() as cursor:
            self.stdout.write('Limpiando esquema public...')
            cursor.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
            cursor.execute("GRANT ALL ON SCHEMA public TO public;")

        self.stdout.write(self.style.SUCCESS('Base de datos vaciada.'))

        # 2. ASEGURAR QUE EXISTEN LAS MIGRACIONES EN DISCO
        self.stdout.write('Generando archivos de migración...')
        # Esto crea los archivos .py si detecta cambios en tus modelos
        call_command('makemigrations', interactive=False)

        # 3. Aplicar las migraciones a la base de datos
        self.stdout.write('Aplicando migraciones a la BD...')
        call_command('migrate', interactive=False)

        # 4. Ejecutar Seeder
        self.stdout.write('Cargando datos iniciales...')
        try:
            call_command('seed_data')
            self.stdout.write(self.style.SUCCESS('Reset y Seed completados con éxito.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error en seeder: {e}'))