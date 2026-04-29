#!/usr/bin/env bash
# Salir si ocurre un error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# RECOLECTAR ESTÁTICOS
python manage.py collectstatic --no-input

# RESET, MIGRATE Y SEED (Todo en uno)
# Nota: En producción real, esto borraría tus datos. 
# Como estamos en desarrollo/fase 1, es perfecto.
python manage.py reset_db

echo "Despliegue finalizado con éxito."