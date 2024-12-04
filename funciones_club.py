import requests
from funcionesVisual import convertir_valor_mercado
from classes.jugador import Jugador

#Intocable
def obtener_jugadores_por_club(club_id):
    url = f"http://127.0.0.1:8000/clubs/{club_id}/players"
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()  # Asegúrate de que no haya errores en la solicitud
        
        # Convertir la respuesta a formato JSON
        jugadores = respuesta.json()  # Esto es ahora un diccionario con la lista de jugadores
        
        # Lista para almacenar los objetos Jugador
        jugadores_objetos = []
        
        # Iterar sobre los jugadores en la respuesta JSON
        for jugador in jugadores['players']:  # Asegúrate de que 'players' esté presente
            # Extraer información del jugador
            jugador_objeto = Jugador(
                id=jugador['id'],
                nombre=jugador['name'],
                posicion=jugador.get('position', 'No disponible'),
                nacionalidad=jugador.get('nationality', 'No disponible'),
                edad=jugador.get('age', 'No disponible'),
                valor_mercado=jugador.get('marketValue', 'No disponible')  # Asegúrate de que 'marketValue' esté presente
            )
            # Agregar el objeto Jugador a la lista
            jugadores_objetos.append(jugador_objeto)
        
        return jugadores_objetos  # Devuelve la lista de objetos Jugador
        
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener jugadores del club {club_id}: {e}")
        return []

def obtener_x_jugadores_top_eq(equipo, x):
    """
    Obtiene los `x` jugadores más valorados de un equipo.
    
    :param equipo: Un objeto de la clase `Equipo` que contiene información sobre el equipo y sus jugadores.
    :param x: Número de jugadores a devolver.
    :return: Una lista de los `x` jugadores más valorados.
    """
    # Obtener los jugadores del equipo
    jugadores = obtener_jugadores_por_club(equipo.get_id())  # Obtener jugadores a partir del ID del equipo

    # Ordenar los jugadores por valor de mercado
    jugadores_ordenados = sorted(
        jugadores,
        key=lambda jugador: convertir_valor_mercado(jugador.get_valor_mercado()),  # Convertir valor de mercado a número
        reverse=True
    )

    # Devolver los x mejores jugadores
    return jugadores_ordenados[:x]