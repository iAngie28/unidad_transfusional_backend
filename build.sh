#!/usr/bin/env bash
# Salir si ocurre un error
set -o errexit

# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Recolectar archivos estáticos (Para que Render sirva CSS/JS del Admin)
python manage.py collectstatic --no-input

# 3. Limpiar, Migrar y Cargar Datos (Usando el comando que creamos)
# Este comando hace el DROP SCHEMA, migrate y seed_data por ti.
python manage.py reset_db