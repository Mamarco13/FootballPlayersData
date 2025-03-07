import requests
from funcionesVisual import convertir_valor_mercado
from classes.jugador import Jugador
from concurrent.futures import ThreadPoolExecutor

# Función para obtener los logros de un jugador
def obtener_logros(jugador_id):
    try:
        response_logros = requests.get(f"http://127.0.0.1:8000/players/{jugador_id}/achievements")
        if response_logros.status_code == 200:
            return response_logros.json().get('achievements', [])
        else:
            print(f"Logros no encontrados para jugador {jugador_id}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener logros para jugador {jugador_id}: {e}")
        return []

def obtener_estadisticas(jugador_id):
    try:
        response_estadisticas = requests.get(f"http://127.0.0.1:8000/players/{jugador_id}/stats")
        if response_estadisticas.status_code == 200:
            estadisticas_completas = response_estadisticas.json().get('stats', [])
            
            # Ordenar las estadísticas por temporada (de más reciente a más antigua)
            estadisticas_sorted = sorted(
                estadisticas_completas,
                key=lambda stat: stat.get('seasonID', '0'),  # Ordenar por 'seasonID'
                reverse=True
            )
            
            # Crear un diccionario para agrupar las competiciones por temporada
            temporadas_incluidas = {}
            for stat in estadisticas_sorted:
                temporada = stat.get('seasonID')
                
                # Solo añadir las tres últimas temporadas (sin romper el ciclo)
                if temporada not in temporadas_incluidas and len(temporadas_incluidas) < 2:
                    temporadas_incluidas[temporada] = []
                
                # Añadir todas las competiciones de la temporada
                if temporada in temporadas_incluidas:
                    temporadas_incluidas[temporada].append(stat)

            # Convertir el diccionario a una lista de estadísticas
            stats_finales = []
            for temporada, stats in temporadas_incluidas.items():
                stats_finales.extend(stats)
            
            return {"stats": stats_finales}
        else:
            print(f"Estadísticas no encontradas para jugador {jugador_id}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener estadísticas para jugador {jugador_id}: {e}")
        return {}


# Función principal para obtener los jugadores de un club
def obtener_jugadores_por_club_simple(club_id):
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
                    valor_mercado=jugador.get('marketValue', 'No disponible')
                )

                jugadores_objetos.append(jugador_objeto)

        return jugadores_objetos
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener jugadores del club {club_id}: {e}")
        return []


# Función principal para obtener los jugadores de un club
def obtener_jugadores_por_club(club_id):
    url = f"http://127.0.0.1:8000/clubs/{club_id}/players"
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        jugadores = respuesta.json()
        jugadores_objetos = []

        # Usar ThreadPoolExecutor para obtener logros y estadísticas en paralelo
        with ThreadPoolExecutor() as executor:
            futures = []  # Lista de futuros para obtener resultados de logros y estadísticas en paralelo

            for jugador in jugadores['players']:
                jugador_objeto = Jugador(
                    id=jugador['id'],
                    nombre=jugador['name'],
                    posicion=jugador.get('position', 'No disponible'),
                    nacionalidad=jugador.get('nationality', 'No disponible'),
                    edad=jugador.get('age', 'No disponible'),
                    valor_mercado=jugador.get('marketValue', 'No disponible')
                )

                # Enviar las solicitudes en paralelo
                logros_future = executor.submit(obtener_logros, jugador['id'])
                estadisticas_future = executor.submit(obtener_estadisticas, jugador['id'])

                # Guardar las futuras respuestas
                futures.append((jugador_objeto, logros_future, estadisticas_future))

            # Esperar a que todas las tareas se completen y actualizar los jugadores con los resultados
            for jugador_objeto, logros_future, estadisticas_future in futures:
                jugador_objeto.logros = logros_future.result()
                jugador_objeto.estadisticas = estadisticas_future.result()

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