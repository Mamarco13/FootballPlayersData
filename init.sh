
# Ejecuta el script AbrirApi.sh
if [ -f "AbrirApi.sh" ]; then
    echo "Ejecutando AbrirApi.sh..."
    bash AbrirApi.sh
else
    echo "No se encontró AbrirApi.sh en la carpeta del proyecto. Saliendo."
    exit 1
fi

# Ejecuta app.py con Python3
if [ -f "app.py" ]; then
    echo "Ejecutando app.py..."
    python3 app.py &
    
    # Espera unos segundos para que el servidor se inicie
    sleep 5
    
    # Abre la página en el navegador por defecto
    echo "Abriendo la página en el navegador..."
    xdg-open "http://127.0.0.1:5000/" || open "http://127.0.0.1:5000/" || start "http://127.0.0.1:5000/"
else
    echo "No se encontró app.py en la carpeta del proyecto. Saliendo."
    exit 1
fi
