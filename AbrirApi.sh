#!/bin/bash

# Cambiar al directorio raíz del proyecto
cd Transfermarkt_API/transfermarkt-api

# Instalar las dependencias
poetry install --no-root

# (Opcional) Agregar el directorio actual al PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Iniciar el servidor de la API usando poetry run
poetry run python app/main.py &

# Abrir la página local de la API en el navegador predeterminado
open http://localhost:8000/


