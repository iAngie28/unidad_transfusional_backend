import os
import sys
import django
from pathlib import Path

# 1. Configuración de rutas para que Python no se pierda
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import UnidadTransfusional, Dominio
from usuarios.models import Rol, Usuario

def ejecutar_seed():
    print("--- 🌱 Iniciando Carga de Datos (Core + Usuarios) ---")

    try:
        # 2. ESQUEMA PÚBLICO (Obligatorio para django-tenants)
        # Este es el "host" del sistema
        public_tenant, created = UnidadTransfusional.objects.get_or_create(
            schema_name='public',
            defaults={'nombre': 'Plataforma Central SGT', 'nivel_complejidad': 'N/A'}
        )
        if created:
            print("✅ Esquema 'public' creado.")
        
        Dominio.objects.get_or_create(
            domain='localhost', 
            tenant=public_tenant, 
            defaults={'is_primary': True}
        )

        # 3. CREAR LA UNIDAD TRANSFUSIONAL (Inquilino)
        # Aquí es donde vivirá la data médica (Pacientes, etc.)
        unidad1, created = UnidadTransfusional.objects.get_or_create(
            schema_name='unidad_norte',
            defaults={'nombre': 'Unidad Transfusional Norte', 'nivel_complejidad': 'Nivel 3'}
        )
        if created:
            print(f"✅ Unidad '{unidad1.nombre}' creada.")

        Dominio.objects.get_or_create(
            domain='unidad1.localhost', 
            tenant=unidad1, 
            defaults={'is_primary': True}
        )

        # 4. CREAR ROLES (En esquema público para login centralizado)
        rol_bio, _ = Rol.objects.get_or_create(
            nombre='BIO', 
            defaults={'descripcion': 'Bioquímico Responsable'}
        )
        Rol.objects.get_or_create(
            nombre='ADM', 
            defaults={'descripcion': 'Administrador de Sistema'}
        )
        print("🔑 Roles configurados.")

        # 5. CREAR EL USUARIO BIOQUÍMICO (Centralizado)
        # Lo vinculamos a la unidad1 para que el Login sepa a dónde mandarlo
        if not Usuario.objects.filter(email='bioquimico@unidad.com').exists():
            usuario = Usuario.objects.create(
                email='bioquimico@unidad.com',
                username='bioquimico@unidad.com',
                first_name='Juan',
                last_name='Pérez',
                rol=rol_bio,
                unidad=unidad1, # <--- La vinculación que pediste
                is_staff=True,
                is_superuser=True,
                esta_activo=True
            )
            usuario.set_password('password123')
            usuario.save()
            print(f"👤 Usuario '{usuario.email}' creado y vinculado a Unidad Norte.")
        else:
            print("ℹ️ El usuario ya existe, omitiendo creación.")

        print("\n--- ✨ Seeder finalizado con éxito ---")

    except Exception as e:
        print(f"\n❌ ERROR EN EL SEEDER: {e}")

if __name__ == "__main__":
    ejecutar_seed()