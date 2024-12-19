from flask import Flask, render_template, request
from classes.liga import Liga
from funcionesLiga import obtener_equipos_por_liga, X_jugadores_ligas
from funciones_club import obtener_jugadores_por_club

app = Flask(__name__)

# Dictionary of leagues with codes and logos
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get selected league codes from the form
        ligas_seleccionadas = request.form.get('ligas', '').split(',')  # Receives a list of league codes
        jugadores_a_mostrar = int(request.form['jugadores'])

        # Process selected leagues and players
        ligas_objetos = []

        for codigo_liga in ligas_seleccionadas:
            for liga_id, liga_info in ligas.items():
                if liga_info['codigo'] == codigo_liga:  # Compare league code
                    nombre = liga_info['nombre']
                    nueva_liga = Liga(codigo_liga, nombre)
                    # Only pass the league code to the function
                    equipos_nueva_liga = obtener_equipos_por_liga(codigo_liga)

                    if equipos_nueva_liga:
                        for eq in equipos_nueva_liga:
                            jugadores_insertar = obtener_jugadores_por_club(eq.get_id())
                            for jugador in jugadores_insertar:
                                jugador.set_team(eq)
                                eq.agregar_jugador(jugador)
                            eq.set_liga(nueva_liga)
                            nueva_liga.agregar_equipo(eq)

                    ligas_objetos.append(nueva_liga)

        # Get players
        top_jugadores = X_jugadores_ligas(ligas_objetos, jugadores_a_mostrar)

        jugadores_display = []
        for jugador in top_jugadores:
            jugadores_display.append({
                'nombre': jugador.get_nombre(),
                'equipo': jugador.get_equipo_actual(),
                'valor_mercado': jugador.get_valor_mercado(),
                'posicion': jugador.get_posicion()
            })

        return render_template('jugadores.html', jugadores=jugadores_display)

    return render_template('index.html', ligas=ligas)

if __name__ == '__main__':
    app.run(debug=True)
