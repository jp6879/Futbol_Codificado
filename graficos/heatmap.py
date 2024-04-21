# Script que grafica el heatmap de un jugador en un partido de fútbol.
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from data_utils.data_handle import data_loader, max_min_scale
from graficos.draw_field import draw_field

def heatmap(player_name : str) -> None:
    """Función que grafica un heatmap de la posición de un jugador en el campo a lo largo del partido.

        Args:
            player_name (str): Nombre del jugador que se quiere graficar su heatmap.

        Returns:
            None

        La función grafica un heatmap de la posición de un jugador en el campo a lo largo del partido.
    """
    # Cargamos los datos de los DataFrames de los equipos locales y visitantes.
    df_local, df_visitante = data_loader()

    # Creamos las listas de los nombres de los jugadores.
    locales = ["Jugador1", "Jugador2", "Jugador3", "Jugador4", "Jugador5", "Jugador6", "Jugador7", "Jugador8", "Jugador9", "Jugador10", "Jugador11", "Jugador12", "Jugador13", "Jugador14"]
    visitantes = ["Jugador15", "Jugador16", "Jugador17", "Jugador18", "Jugador19", "Jugador20", "Jugador21", "Jugador22", "Jugador23", "Jugador24", "Jugador25", "Jugador26", "Jugador27", "Jugador28"]

    total_jugadores = np.concatenate((locales, visitantes))

    if not player_name in total_jugadores:
        raise ValueError(f"El jugador {player_name} tiene que estar en lista de jugadores")
    
    # Creamos la figura y el eje.
    fig, ax = draw_field()

    if player_name in locales:
        # Extraemos las posiciones x e y del jugador, tiramos las que no tienen datos y escaleamos a las dimensiones de la cancha.
        jugador_x = df_local[player_name + 'x'].dropna().values * 105
        jugador_y = df_local[player_name + 'y'].dropna().values * 68
    elif player_name in visitantes:
        # Extraemos las posiciones x e y del jugador, tiramos las que no tienen datos y escaleamos a las dimensiones de la cancha.
        jugador_x = df_visitante[player_name + 'x'].dropna().values * 105
        jugador_y = df_visitante[player_name + 'y'].dropna().values * 68

    # Calculamos el histograma 2D.
    hist, _, _ = np.histogram2d(jugador_x, jugador_y, bins=[105, 68], range=[[0, 105], [0, 68]]) # Pongo los mismos bins que la cancha

    # Para graficar con seaborn paso a un DataFrame
    hist_df = pd.DataFrame(hist.T.tolist())

    # Escalamos los datos para que estén entre 0 y 1 para poder visaualizarlos mejor.
    for col in hist_df.columns:
        hist_df[col] = max_min_scale(hist_df[col])

    fig, ax = draw_field()
    sns.heatmap(hist_df, cmap='hot', alpha = 0.5, annot = False, cbar = False ,ax=ax)
    ax.set_title(f"Mapa de calor del {player_name}")
    plt.show()