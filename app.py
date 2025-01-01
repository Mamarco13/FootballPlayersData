from flask import Flask, render_template, request
from classes.liga import Liga
from funcionesLiga import obtener_equipos_por_liga, X_jugadores_ligas
from funciones_club import obtener_jugadores_por_club, obtener_jugadores_por_club_simple
from funcionesVisual import convertir_valor_mercado
from flask import render_template
from funcionesJugadores import mostrar_estadisticas_grafico, completar_jugador  # Importa la función de grafico.py


app = Flask(__name__)

# Diccionario de ligas (ya lo tienes)
ligas = {
    0: {"nombre": "LaLiga", "codigo": "ES1", "logo": "https://media.gq.com.mx/photos/647df9eacd18d7f1c032cf77/master/w_1600%2Cc_limit/LaLiga_logo.jpg"},
    1: {"nombre": "LaLiga Hypermotion", "codigo": "ES2", "logo": "https://image.discovery.indazn.com/ca/v2/ca/image?id=fc5ca30c-f166-4a66-b520-b042b4a1d6e5&quality=70"},
    2: {"nombre": "Premier League", "codigo": "GB1", "logo": "https://www.classicfootballshirts.co.uk/cdn-cgi/image/fit=pad,q=70,f=webp//pub/media/catalog/product//p/r/prem-23.jpg"},
    3: {"nombre": "Championship", "codigo": "GB2", "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-jsCrL9uViiHZoazGjJYXfdsQQP7xu8smYw&s"},
    4: {"nombre": "Bundesliga", "codigo": "L1", "logo": "https://logowik.com/content/uploads/images/bundesliga7083.jpg"},
    5: {"nombre": "Bundesliga2", "codigo": "L2", "logo": "https://www.11teamsports.com/cdn-cgi/image/format=webp,width=601/media/58/1e/4b/1625369681/dfl-badge-offizielles-bundesliga-logo-fuer-die-zweite-bundesliga-dfl-b2576-02-erw.png"},
    6: {"nombre": "Serie A", "codigo": "IT1", "logo": "https://www.chefstudio.it/img/blog/logo-serie-a/logo-serie-a.jpg"},
    7: {"nombre": "Serie B", "codigo": "IT2", "logo": "https://www.fccrotone.it/wp-content/uploads/2016/03/logo-serie-b.gif"},
    8: {"nombre": "Ligue 1", "codigo": "FR1", "logo": "https://1000logos.net/wp-content/uploads/2024/04/ligue1-mcd-logo.jpeg"},
    9: {"nombre": "Ligue 2", "codigo": "FR2", "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ5y4ysYOxYZznSIUCw1Fwmg1CT1fADIToFGQ&s"}
}

# Diccionario de clubes
clubes = {
    0: {"nombre": "Granada CF", "codigo": "16795", "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlMlV11fmBvnB7UA6QKpLV7XqT8TpiDjq0fg&s"},
    1: {"nombre": "Real Madrid", "codigo": "418", "logo": "https://estaticos-cdn.prensaiberica.es/clip/c8717efc-31eb-48fb-b01b-bdd1a43dfde1_alta-libre-aspect-ratio_default_0.jpg"},
    2: {"nombre": "FC Barcelona", "codigo": "131", "logo": "https://logowik.com/content/uploads/images/802_fcbarcelona.jpg"},
}

# Lista global para almacenar jugadores
todos_los_jugadores = []

@app.route('/')
def index():
    return render_template('index.html', ligas=ligas)

@app.route('/seleccion_liga', methods=['GET', 'POST'])
def seleccion_liga():
    global todos_los_jugadores  # Usar la variable global
    todos_los_jugadores = []  # Reiniciar cada vez que se hace una nueva selección

    if request.method == 'POST':
        ligas_seleccionadas = request.form.get('ligas', '').split(',')  # Recibe una lista de códigos de ligas
        jugadores_a_mostrar = int(request.form['jugadores'])

        ligas_objetos = []

        for codigo_liga in ligas_seleccionadas:
            for liga_id, liga_info in ligas.items():
                if liga_info['codigo'] == codigo_liga:
                    nombre = liga_info['nombre']
                    nueva_liga = Liga(codigo_liga, nombre)
                    equipos_nueva_liga = obtener_equipos_por_liga(codigo_liga)

                    if equipos_nueva_liga:
                        for eq in equipos_nueva_liga:
                            jugadores_insertar = obtener_jugadores_por_club_simple(eq.get_id())
                            for jugador in jugadores_insertar:
                                jugador.set_team(eq)
                                eq.agregar_jugador(jugador)
                                todos_los_jugadores.append(jugador)  # Agregar a la lista global
                            # Agregar a la lista global
                            eq.set_liga(nueva_liga)
                            nueva_liga.agregar_equipo(eq)

                    ligas_objetos.append(nueva_liga)

        top_jugadores = X_jugadores_ligas(ligas_objetos, jugadores_a_mostrar)

        jugadores_display = []
        for jugador in top_jugadores:
            jugadores_display.append({
                'id': jugador.get_id(),
                'nombre': jugador.get_nombre(),
                'equipo': jugador.get_equipo_actual(),
                'valor_mercado': jugador.get_valor_mercado(),
                'posicion': jugador.get_posicion(),
                'logros': jugador.get_logros(),
                'estadisticas': jugador.get_estadisticas()
            })


        return render_template('jugadores.html', jugadores=jugadores_display)

    # Para el método GET
    return render_template('seleccion_liga.html', ligas=ligas)

@app.route('/profile/<int:jugador_id>')
def perfil_jugador(jugador_id):
    jugador_encontrado = None

    # Buscar el jugador en la lista global
    for jugador in todos_los_jugadores:
        if str(jugador.get_id()) == str(jugador_id):
            #jugador_encontrado = jugador

            #COMPLETAR JUGADOR MEJOR QUE LO DE ARRIBA
            jugador_encontrado = completar_jugador(jugador)



            break

    if jugador_encontrado is None:
        return render_template('error.html', mensaje="Jugador no encontrado"), 404

    # Procesar logros
    logros_procesados = []
    for logro in jugador_encontrado.get_logros():
        detalles = ", ".join(
            f"{detalle.get('season', {}).get('name', 'Unknown')} - {detalle.get('competition', {}).get('name', detalle.get('club', {}).get('name', 'Unknown'))}"
            for detalle in logro.get('details', [])
        )
        logros_procesados.append(f"{logro['title']} ({logro['count']}) - {detalles}")

    # Procesar estadísticas y filtrar las últimas tres temporadas
    estadisticas_procesadas = {}
    stats = jugador_encontrado.get_estadisticas()#.get('stats', [])

    # Ordenar estadísticas por temporada de forma descendente
    stats_sorted = sorted(
        stats,
        key=lambda stat: stat.get('seasonID', '0'),  # Ordenar por 'seasonID'
        reverse=True
    )

    # Agrupar las competiciones por temporada
    temporadas_incluidas = {}
    contador_temporadas = 0  # Contador de temporadas distintas

    for stat in stats_sorted:
        temporada = stat.get('seasonID')
        if temporada not in temporadas_incluidas:
            if contador_temporadas < 2:  # Limitar a las dos últimas temporadas
                temporadas_incluidas[temporada] = []
                contador_temporadas += 1

        # Agregar la competencia de la temporada actual si la temporada ya está incluida
        if temporada in temporadas_incluidas:
            temporadas_incluidas[temporada].append(stat)

    # Procesar estadísticas para mostrar todas las competiciones de las dos últimas temporadas
    for temporada, stats_por_temporada in temporadas_incluidas.items():
        for stat in stats_por_temporada:
            if isinstance(stat, dict):  # Verificar si es un diccionario
                key = f"{stat.get('competitionName', 'Unknown')} ({stat.get('seasonID', 'Unknown')})"
                value = (
                    f"Matches: {stat.get('appearances', '0')}, Goals: {stat.get('goals', '0')}, "
                    f"Assists: {stat.get('assists', '0')}, Minutes: {stat.get('minutesPlayed', '0')}"
                )
                estadisticas_procesadas[key] = value
            elif isinstance(stat, str):  # Si ya es una cadena
                estadisticas_procesadas[stat] = "No additional data available"
            else:  # Caso inesperado
                print(f"Formato inesperado en estadística: {stat}")
                estadisticas_procesadas["Unknown"] = "Formato desconocido"


    # Generar el gráfico de estadísticas en base64
    imagen_base64 = mostrar_estadisticas_grafico(jugador_encontrado.get_estadisticas())

    # Actualizar los datos del jugador
    jugador_encontrado.logros = logros_procesados
    jugador_encontrado.estadisticas = estadisticas_procesadas
    jugador_encontrado.imagen_base64 = imagen_base64  # Agregar la imagen codificada en base64

    # Renderizar la plantilla y pasar la imagen
    return render_template('profile.html', jugador=jugador_encontrado, imagen_base64=imagen_base64)




@app.route('/seleccion_club', methods=['GET', 'POST'])
def seleccion_club():
    global todos_los_jugadores  # Usar la variable global
    todos_los_jugadores = []  # Reiniciar cada vez que se hace una nueva selección

    if request.method == 'POST':
        # Obtener los clubes seleccionados desde el formulario
        clubes_seleccionados = request.form.get('clubes', '').split(',')  # Se espera una lista separada por comas
        jugadores_a_mostrar = int(request.form['jugadores'])  # Número de jugadores a mostrar

        jugadores_display = []

        # Obtener los jugadores de todos los clubes seleccionados
        for codigo_club in clubes_seleccionados:
            for club_id, club_info in clubes.items():  # Asumiendo que 'clubes' es un diccionario con info de cada club
                if club_info['codigo'] == codigo_club:
                    club_objeto = club_info  # Asegúrate de tener toda la información del club

                    # Obtener los jugadores de este club
                    jugadores = obtener_jugadores_por_club(club_objeto['codigo'])

                    for jugador in jugadores:
                        jugador.set_team_name(club_objeto['nombre'])
                        todos_los_jugadores.append(jugador)  # Agregar a la lista global

                        # Añadir los jugadores a la lista
                        jugadores_display.append({
                            'id': jugador.get_id(),
                            'nombre': jugador.get_nombre(),
                            'equipo': jugador.get_equipo_actual(),
                            'valor_mercado': jugador.get_valor_mercado(),
                            'posicion': jugador.get_posicion(),
                            'logros': jugador.get_logros(),
                            'estadisticas': jugador.get_estadisticas()
                        })


        # Ordenamos todos los jugadores de todos los clubes seleccionados por valor de mercado
        jugadores_display.sort(key=lambda x: convertir_valor_mercado(x['valor_mercado']), reverse=True)

        # Limitar la lista a los 'X' jugadores más valiosos
        jugadores_display = jugadores_display[:jugadores_a_mostrar]

        
        # Renderizamos la plantilla con la lista de jugadores seleccionados y ordenados
        return render_template('jugadores.html', jugadores=jugadores_display)

    # Si el método es GET, simplemente renderizamos la página para seleccionar los clubes
    return render_template('seleccion_club.html', clubes=clubes)

if __name__ == '__main__':
    app.run(debug=True)