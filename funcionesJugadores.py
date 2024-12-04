import requests

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



