import requests
from funcionesVisual import convertir_valor_mercado
from classes.jugador import Jugador

def obtener_jugadores_por_club(club_id):
    url = f"http://127.0.0.1:8000/clubs/{club_id}/players"
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        jugadores = respuesta.json()
        jugadores_objetos = []

        for jugador in jugadores['players']:
            jugador_objeto = Jugador(
                id=jugador['id'],
                nombre=jugador['name'],
                posicion=jugador.get('position', 'No disponible'),
                nacionalidad=jugador.get('nationality', 'No disponible'),
                edad=jugador.get('age', 'No disponible'),
                valor_mercado=jugador.get('marketValue', 'No disponible')
            )

            # Obtener logros
            try:
                response_logros = requests.get(f"http://127.0.0.1:8000/players/{jugador['id']}/achievements")
                if response_logros.status_code == 200:
                    jugador_objeto.logros = response_logros.json().get('achievements', [])
                else:
                    print(f"Logros no encontrados para jugador {jugador['name']} ({jugador['id']})")
            except requests.exceptions.RequestException as e:
                print(f"Error al obtener logros para jugador {jugador['name']} ({jugador['id']}): {e}")

            # Obtener estadísticas (solo las tres últimas temporadas)
            try:
                response_estadisticas = requests.get(f"http://127.0.0.1:8000/players/{jugador['id']}/stats")
                if response_estadisticas.status_code == 200:
                    estadisticas_completas = response_estadisticas.json().get('stats', [])
                    # Tomar solo las tres primeras entradas
                    jugador_objeto.estadisticas = {"stats": estadisticas_completas[:3]}
                else:
                    print(f"Estadísticas no encontradas para jugador {jugador['name']} ({jugador['id']})")
            except requests.exceptions.RequestException as e:
                print(f"Error al obtener estadísticas para jugador {jugador['name']} ({jugador['id']}): {e}")

            # Debug
            print(f"Jugador agregado: {jugador_objeto.get_nombre()},  {jugador_objeto.get_logros()}, {jugador_objeto.get_estadisticas()}\n")

            jugadores_objetos.append(jugador_objeto)
        
        return jugadores_objetos
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