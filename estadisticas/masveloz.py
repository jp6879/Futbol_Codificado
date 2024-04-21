import findiff as fd
import numpy as np
from data_utils.data_handle import data_loader, clean_data

# Cargamos los datos.
df_local, df_visitante = data_loader()


# Función auxiliar para el calculo del mas veloz del partido.
def calcula_velocidad(player_name : str) -> float:
    """Función que calucla la velocidad de un jugador a lo largo del partido.

        Args:
            player_name (str): Nombre del jugador del que se quiere calcular la velocidad.
        
        Returns:
            float: Velocidad media del jugador a lo largo del partido.
        
        El calculo de la velocidad se realiza haciendo la derivada de las posiciones x e y en función del tiempo y calculando la velocidad total.
    """

    # Creamos las listas de los nombres de los jugadores.
    locales = ["Jugador1", "Jugador2", "Jugador3", "Jugador4", "Jugador5", "Jugador6", "Jugador7", "Jugador8", "Jugador9", "Jugador10", "Jugador11", "Jugador12", "Jugador13", "Jugador14"]
    visitantes = ["Jugador15", "Jugador16", "Jugador17", "Jugador18", "Jugador19", "Jugador20", "Jugador21", "Jugador22", "Jugador23", "Jugador24", "Jugador25", "Jugador26", "Jugador27", "Jugador28"]

    # Chequeamos que el nombre ingresado esté en la lista de jugadores.
    if player_name in locales:
        jugador = df_local[["Tiempo [s]" , player_name + "x", player_name + "y"]]
    elif player_name in visitantes:
        jugador = df_visitante[["Tiempo [s]" ,player_name + "x", player_name + "y"]]
    else:
        raise ValueError(f"El jugador {player_name} no está en la lista de jugadores")
    
    # Tiramos los valores NaN.
    jugador = jugador.dropna()

    # Escaleamos a los valores de la cancha y extraemos las posiciones x, y.
    jugador_x = jugador[player_name + "x"].values * 105
    jugador_y = jugador[player_name + "y"].values * 68
    tiempo = jugador["Tiempo [s]"].values
    # Derivamos para encontrar las velocidades v_x y v_y, como scipy dejó de mantener la funcion de derivada, usamos FinDiff.
    dx = tiempo[1] - tiempo[0]
    d_dx = fd.FinDiff(0, dx, 1)
    df_dx = d_dx(jugador_x)
    df_dy = d_dx(jugador_y)

    # Calculamos la velocidad total.
    vel = np.sqrt(df_dx**2 + df_dy**2)

    # Devolvemos la media de la velocidad durante el partido.
    return np.mean(vel)


def encuentra_mas_veloz():
    """Función que encuentra el jugador más veloz del partido."""

    # Creamos las listas de los nombres de los jugadores.
    locales = ["Jugador1", "Jugador2", "Jugador3", "Jugador4", "Jugador5", "Jugador6", "Jugador7", "Jugador8", "Jugador9", "Jugador10", "Jugador11", "Jugador12", "Jugador13", "Jugador14"]
    visitantes = ["Jugador15", "Jugador16", "Jugador17", "Jugador18", "Jugador19", "Jugador20", "Jugador21", "Jugador22", "Jugador23", "Jugador24", "Jugador25", "Jugador26", "Jugador27", "Jugador28"]

    # Concatenamos los nombres de los jugadores locales y visitantes.
    jugadores = locales + visitantes

    # Calculamos las velocidades de cada jugador y devolvemos la velocidad máxima y el nombre del jugador.
    velocidades = [calcula_velocidad(jugador) for jugador in jugadores]

    return max(velocidades), jugadores[np.argmax(velocidades)]