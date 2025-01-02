import requests
import io
import base64
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
#matplotlib.use('Agg')  # Usar un backend no interactivo para evitar errores de GUI
import matplotlib.ticker as mticker

def mostrar_estadisticas_grafico(estadisticas):
    # Validar el formato de entrada
    if isinstance(estadisticas, list):
        stats = estadisticas
    elif isinstance(estadisticas, dict):
        stats = estadisticas.get("stats", [])
    else:
        print("Formato de estadísticas no reconocido.")
        return None

    if not stats:
        print("No hay estadísticas para mostrar.")
        return None

    # Convertir a DataFrame
    df = pd.DataFrame(stats)

    # Verificar columnas requeridas
    required_columns = {'competitionName', 'seasonID', 'goals', 'assists', 'appearances', 'minutesPlayed'}
    if not required_columns.issubset(df.columns):
        print("Faltan datos necesarios para generar el gráfico.")
        return None

    # Convertir columnas a tipos adecuados
    df['goals'] = pd.to_numeric(df['goals'], errors='coerce').fillna(0).astype(int)
    df['assists'] = pd.to_numeric(df['assists'], errors='coerce').fillna(0).astype(int)
    df['appearances'] = pd.to_numeric(df['appearances'], errors='coerce').fillna(0).astype(int)
    # Corregir los minutos jugados multiplicando por 1000 si están en formato decimal
    df['minutesPlayed'] = pd.to_numeric(df['minutesPlayed'].replace({r"[^\d.]": ""}, regex=True), errors='coerce').fillna(0).apply(lambda x: x * 1000 if x < 10 else x).astype(int)
    df['competitionName'] = df['competitionName'].astype(str)
    df['seasonID'] = df['seasonID'].astype(str)

    # Filtrar estadísticas por las dos temporadas más recientes
    temporadas_mas_recientes = df['seasonID'].drop_duplicates().sort_values(ascending=False).head(2)
    df = df[df['seasonID'].isin(temporadas_mas_recientes)]

    if df.empty:
        print("No hay estadísticas para las últimas dos temporadas.")
        return None

    # Crear columna combinada para etiquetas
    df['competition_season'] = df['competitionName'] + " (" + df['seasonID'] + ")"

    # Crear gráficos con Pandas
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Gráfico de Goles
    df.plot.bar(x='competition_season', y='goals', color='skyblue', ax=axes[0, 0], legend=False)
    axes[0, 0].set_title('Goals - Last 2 Seasons')
    axes[0, 0].set_ylabel('Goals')

    # Gráfico de Asistencias
    df.plot.bar(x='competition_season', y='assists', color='lightgreen', ax=axes[0, 1], legend=False)
    axes[0, 1].set_title('Assists - Last 2 Seasons')
    axes[0, 1].set_ylabel('Assists')

    # Gráfico de Apariciones
    df.plot.bar(x='competition_season', y='appearances', color='coral', ax=axes[1, 0], legend=False)
    axes[1, 0].set_title('Appearances - Last 2 Seasons')
    axes[1, 0].set_ylabel('Appearances')

    # Gráfico de Minutos Jugados
    df.plot.bar(x='competition_season', y='minutesPlayed', color='lightcoral', ax=axes[1, 1], legend=False)
    axes[1, 1].set_title('Minutes Played - Last 2 Seasons')
    axes[1, 1].set_ylabel('Minutes Played')

    # Ajustar el límite superior del eje Y para minutos jugados
    ylim_upper = df['minutesPlayed'].max() * 1.2
    axes[1, 1].set_ylim(0, ylim_upper)

    # Formatear etiquetas del eje Y para minutos jugados
    axes[1, 1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))

    # Ajustar diseño y guardar el gráfico
    for ax in axes.flatten():
        ax.tick_params(axis='x', rotation=45, labelsize=10)

    plt.tight_layout()

    # Guardar el gráfico en memoria como PNG
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png', dpi=100)
    plt.close()

    img_stream.seek(0)
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


def completar_jugador(jugador):
    """
    Completa un objeto Jugador con su Nacionalidad, Edad, Logros y Estadísticas.
    """
    jugador_id = jugador.get_id()
    
    try:
        # Obtener perfil del jugador (incluye edad y nacionalidad)
        profile_url = f"http://127.0.0.1:8000/players/{jugador_id}/profile"
        response_profile = requests.get(profile_url)
        if response_profile.status_code == 200:
            profile_data = response_profile.json()
            jugador.set_pais(profile_data.get("citizenship"))
            jugador.edad = profile_data.get("age")
        else:
            print(f"No se pudo obtener el perfil del jugador {jugador_id}")

        # Obtener logros del jugador
        achievements_url = f"http://127.0.0.1:8000/players/{jugador_id}/achievements"
        response_achievements = requests.get(achievements_url)
        if response_achievements.status_code == 200:
            achievements_data = response_achievements.json().get('achievements', [])
            jugador.logros = achievements_data
        else:
            print(f"No se pudieron obtener los logros del jugador {jugador_id}")

        # Obtener estadísticas del jugador
        stats_url = f"http://127.0.0.1:8000/players/{jugador_id}/stats"
        response_stats = requests.get(stats_url)
        if response_stats.status_code == 200:
            stats_data = response_stats.json().get('stats', [])
            if isinstance(stats_data, list):
                jugador.estadisticas = stats_data
            else:
                jugador.estadisticas = [stats_data]  # Asegurar que siempre sea lista
        else:
            print(f"No se pudieron obtener las estadísticas del jugador {jugador_id}")


    except requests.exceptions.RequestException as e:
        print(f"Error al completar datos del jugador {jugador_id}: {e}")
    
    return jugador
