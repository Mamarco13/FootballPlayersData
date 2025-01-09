#!/bin/bash

# Cambiar al directorio raíz del proyecto
cd Transfermarkt_API/transfermarkt-api

# Instalar las dependencias
poetry install --no-root

# (Opcional) Agregar el directorio actual al PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Iniciar el servidor de la API usando poetry run, forzando el puerto 8000
poetry run python app/main.py --port 8000 & 
