from funciones_club import obtener_jugadores_por_club
from funcionesVisual import convertir_valor_mercado
from classes.equipo import Equipo
import requests

#Intocable
def obtener_equipos_por_liga(liga_id):
    url = f"http://127.0.0.1:8000/competitions/{liga_id}/clubs"
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        datos_liga = respuesta.json()  # Datos de la liga incluyendo los equipos
        equipos = datos_liga.get('clubs', [])  # Lista de equipos
        
        # Convertir cada equipo en un objeto Equipo
        equipos_objetos = []
        for eq in equipos:
            equipo_objeto = Equipo(
                id=eq['id'], 
                nombre=eq['name']
            )
            equipos_objetos.append(equipo_objeto)
        
        return equipos_objetos
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener equipos de la liga {liga_id}: {e}")
        return []

def obtener_ids_equipos_por_liga(liga_id):
    equipos = obtener_equipos_por_liga(liga_id)
    ids_equipos = [equipo.get_id() for equipo in equipos]  # Extraer solo los IDs
    return ids_equipos

def X_jugadores_ligas(ligas, x):
    jugadores = []
    
    # Agregar todos los jugadores de las ligas a la lista
    for liga in ligas:
        jugadores_agregar = liga.obtener_todos_los_jugadores()
        for jugador in jugadores_agregar:
            jugadores.append(jugador)
    
    # Ordenar los jugadores por valor de mercado (de mayor a menor)
    jugadores_ordenados = sorted(
        jugadores,
        key=lambda jugador: convertir_valor_mercado(jugador.get_valor_mercado()),  # Asegurar que el valor sea numérico
        reverse=True
    )
    
    # Seleccionar los 'x' jugadores más valiosos
    top_jugadores = jugadores_ordenados[:x]
    
    # Devolver o imprimir los jugadores seleccionados
    return top_jugadores
