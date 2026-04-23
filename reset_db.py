import os
import psycopg2
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# --- CONFIGURACIÓN ---
# Asegúrate de que estos datos sean los mismos de tu settings.py
DB_NAME = 'unidad_transfusional_db' 
DB_USER = 'postgres'
DB_PASS = 'adm123' 
DB_HOST = '127.0.0.1'
DB_PORT = '5432'

def clean_migrations():
    print("--- 🗑️ Borrando archivos de migraciones ---")
    # Solo las apps que tenemos activas actualmente
    target_apps = ['core', 'usuarios'] 
    
    for app in target_apps:
        migration_dir = os.path.join(app, "migrations")
        if os.path.exists(migration_dir):
            for file in os.listdir(migration_dir):
                # No borramos el __init__.py porque es lo que identifica a la carpeta como módulo
                if file != "__init__.py" and os.path.isfile(os.path.join(migration_dir, file)):
                    file_path = os.path.join(migration_dir, file)
                    os.remove(file_path)
                    print(f"Eliminado: {file_path}")

def reset_database():
    print(f"--- 🔄 Reiniciando base de datos: {DB_NAME} ---")
    try:
        # Conexión a la db 'postgres' para poder borrar la otra
        conn = psycopg2.connect(
            dbname='postgres', user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Matamos cualquier conexión activa a la base de datos para que nos deje borrarla
        cursor.execute(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{DB_NAME}'
              AND pid <> pg_backend_pid();
        """)
        
        cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME};")
        cursor.execute(f"CREATE DATABASE {DB_NAME};")
        
        cursor.close()
        conn.close()
        print("✅ Base de datos recreada.")
    except Exception as e:
        print(f"❌ Error al resetear DB: {e}")
        sys.exit(1)

def run_django_commands():
    print("--- 🏗️ Generando Migraciones ---")
    # TRUCO CLAVE: Ejecutamos makemigrations sin especificar apps 
    # para que Django resuelva las dependencias entre ellas automáticamente.
    os.system("python manage.py makemigrations")
    
    print("--- 🧬 Aplicando Esquemas ---")
    # Esto aplica primero 'public' y luego los tenants que existan
    os.system("python manage.py migrate_schemas")

if __name__ == "__main__":
    clean_migrations()
    reset_database()
    run_django_commands()
    print("\n🚀 PROCESO COMPLETADO. Ahora ejecuta: python seed_inicial.py")