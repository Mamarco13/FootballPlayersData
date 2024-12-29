import requests

import io
import base64
import pandas as pd
import matplotlib.pyplot as plt


def mostrar_estadisticas_grafico(estadisticas):
    # Convertir las estadísticas a un DataFrame de pandas
    stats = estadisticas.get("stats", [])
    
    if not stats:
        print("No hay estadísticas para mostrar.")
        return None
    
    # Crear un DataFrame a partir de las estadísticas
    df = pd.DataFrame(stats)
    
    # Asegurarse de que las columnas necesarias están presentes
    if 'competitionName' not in df.columns or 'seasonID' not in df.columns:
        print("Faltan datos necesarios para generar el gráfico.")
        return None

    # Convertir columnas numéricas a su tipo adecuado (int o float)
    df['goals'] = pd.to_numeric(df['goals'], errors='coerce').fillna(0).astype(int)
    df['assists'] = pd.to_numeric(df['assists'], errors='coerce').fillna(0).astype(int)
    df['appearances'] = pd.to_numeric(df['appearances'], errors='coerce').fillna(0).astype(int)
    df['minutesPlayed'] = pd.to_numeric(df['minutesPlayed'], errors='coerce').fillna(0).astype(int)

    # Asegurarse de que las columnas estén en formato correcto (str)
    df['competitionName'] = df['competitionName'].astype(str)
    df['seasonID'] = df['seasonID'].astype(str)
    
    # Crear un gráfico de barras para cada tipo de estadística (goles, asistencias, etc.)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Gráfico de Goles
    axes[0, 0].bar(df['competitionName'] + " (" + df['seasonID'] + ")", df['goals'], color='skyblue')
    axes[0, 0].set_title('Goals per Competition')
    axes[0, 0].set_ylabel('Goals')
    axes[0, 0].tick_params(axis='x', rotation=45)

    # Gráfico de Asistencias
    axes[0, 1].bar(df['competitionName'] + " (" + df['seasonID'] + ")", df['assists'], color='lightgreen')
    axes[0, 1].set_title('Assists per Competition')
    axes[0, 1].set_ylabel('Assists')
    axes[0, 1].tick_params(axis='x', rotation=45)

    # Gráfico de Apariciones
    axes[1, 0].bar(df['competitionName'] + " (" + df['seasonID'] + ")", df['appearances'], color='coral')
    axes[1, 0].set_title('Appearances per Competition')
    axes[1, 0].set_ylabel('Appearances')
    axes[1, 0].tick_params(axis='x', rotation=45)

    # Gráfico de Minutos Jugados
    axes[1, 1].bar(df['competitionName'] + " (" + df['seasonID'] + ")", df['minutesPlayed'], color='lightcoral')
    axes[1, 1].set_title('Minutes Played per Competition')
    axes[1, 1].set_ylabel('Minutes Played')
    axes[1, 1].tick_params(axis='x', rotation=45)

    # Ajustar espacio entre los subgráficos
    plt.tight_layout()
    
    # Guardar el gráfico en memoria como una imagen en formato PNG
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png')
    plt.close()  # Cerrar el gráfico

    # Convertir la imagen a base64
    img_stream.seek(0)  # Volver al principio del stream
    img_base64 = base64.b64encode(img_stream.getvalue()).decode('utf-8')
    
    return img_base64


def obtener_valor_mercado(player_id: str):
    url = f"http://127.0.0.1:8000/players/{player_id}/market_value"  # Ajusta la URL con el prefijo /players
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()  # Obtén los datos del JSON
        return data.get("marketValue", "Valor de mercado no disponible")  # Devuelve solo el valor de mercado
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el valor de mercado del jugador {player_id}: {e}")
        return None

def convertir_valor_mercado(valor_mercado):
    # Eliminamos el símbolo '€' y convertimos la cantidad a número
    if valor_mercado is None or valor_mercado == 'No disponible':
        return 0  # En caso de que no haya valor de mercado
    valor_mercado = valor_mercado.strip().replace('€', '').replace(' ', '')
    
    if 'm' in valor_mercado.lower():  # Para millones
        return float(valor_mercado.lower().replace('m', '')) * 1_000_000
    elif 'k' in valor_mercado.lower():  # Para miles
        return float(valor_mercado.lower().replace('k', '')) * 1_000
    else:
        return float(valor_mercado)  # Para valores numéricos directos



