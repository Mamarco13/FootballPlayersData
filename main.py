from classes.liga import Liga
from funcionesLiga import obtener_equipos_por_liga, X_jugadores_ligas
from funciones_club import obtener_jugadores_por_club

# IDs de las ligas
ligas_ids = {
    0: ("LaLiga", "ES1"),
    1: ("LaLiga Hypermotion", "ES2"),
    2: ("Premier League", "GB1"),
    3: ("Championship", "GB2"),
    4: ("Bundesliga", "L1"),
    5: ("Bundesliga2", "L2"),
    6: ("Serie A", "IT1"),
    7: ("Serie B", "IT2"),
    8: ("Ligue 1", "FR1"),
    9: ("Ligue 2", "FR2")
}

# Mensaje para el usuario
print("First of all, you should select how many leagues you want in your database:")
print("\tLaLiga : 0\n\tLaLiga Hypermotion: 1\n\tPremier League : 2\n\tChampionship: 3")
print("\tBundesliga : 4\n\tBundesliga2: 5\n\tSerie A : 6\n\tSerie B : 7")
print("\tLigue 1: 8\n\tLigue 2: 9")

# Entrada del usuario
selecciones = input("Select the leagues you want (separate numbers by commas): ")

# Convertir la entrada a una lista de enteros
try:
    ligas_seleccionadas = [int(num.strip()) for num in selecciones.split(",")]
except ValueError:
    print("Error: Please introduce the numbers separated by a ','.")
    ligas_seleccionadas = []

# Crear instancias de las ligas seleccionadas
ligas_objetos = []
for num in ligas_seleccionadas:
    if num in ligas_ids:
        nombre, id_liga = ligas_ids[num]
        #Crear liga
        nueva_liga = Liga(id_liga, nombre)
        #Insertar equipos en la liga
        equipos_nueva_liga = obtener_equipos_por_liga(id_liga)
        for eq in equipos_nueva_liga:
            #Insertar jugadores en equipos
            jugadores_insertar = obtener_jugadores_por_club(eq.get_id())
            for jugador in jugadores_insertar:
                jugador.set_team(eq)
                eq.agregar_jugador(jugador)
            eq.set_liga(nueva_liga)
            nueva_liga.agregar_equipo(eq)
        ligas_objetos.append(nueva_liga)
    else:
        print(f"Invalid league number: {num}")



# Solicitar al usuario cuántos jugadores mostrar
jugadores_a_mostrar = input("\nNumber of players to display on screen: ")
try:
    jugadores_a_mostrar = int(jugadores_a_mostrar)  # Convertir a entero
    if jugadores_a_mostrar <= 0:
        raise ValueError("El número de jugadores debe ser mayor que 0.")
except ValueError as e:
    print(f"Error: {e}")
    jugadores_a_mostrar = 10  # Valor por defecto

# Obtener los mejores jugadores de todas las ligas seleccionadas
#top_jugadores = obtener_x_jugadores_liga(ligas_seleccionadas, jugadores_a_mostrar)
top_jugadores = X_jugadores_ligas(ligas_objetos, jugadores_a_mostrar)
# Mostrar los jugadores
for jugador in top_jugadores:
    print(jugador)
    print("\n")
