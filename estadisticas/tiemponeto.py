# Script que calcula el tiempo neto jugado en el partido.
import numpy as np
import math
from data_utils.data_handle import data_loader

def tiempo_neto() -> tuple[float, float]:
    """Función que calucla el tiempo neto de juego  definido como el tiempo durante el cual el balón está dentro del campo de juego) 
        y el tiempo no jugado (definido como el tiempo durante el cual el balón no está dentro del campo de juego) en minutos.

        Returns:
            tiempo_jugado (float): tiempo neto jugado en minutos
            tiempo_no_jugado (float): tiempo no jugado en minutos
                        
    """
    # Cargamos los datos.
    df_local, _ = data_loader()

    # Encontramos los momentos antes y despuén en los que la pelota no está en el campo y tiene valor NaN y los guardamos en una lista.
    tiempos_hasta_salida = [0]

    for i in range(610, len(df_local["Pelotax"]) - 1):
        if math.isnan(df_local["Pelotax"][i]) and not math.isnan(df_local["Pelotax"][i-1]):
            tiempos_hasta_salida.append(df_local["Tiempo [s]"][i-1])
        if math.isnan(df_local["Pelotax"][i]) and not math.isnan(df_local["Pelotax"][i+1]):
            tiempos_hasta_salida.append(df_local["Tiempo [s]"][i+1])

    # Calculamos las diferencias entre los momentos antes y después de que la pelota salga del campo, así tenemos una lista con segundos jugados en los lugares pares y segundos no jugados en los impares
    diferencias = np.diff(tiempos_hasta_salida)

    # Sumamos los segundos jugados y no jugados y devolvemos el tiempo jugado y no jugado en minutos.
    tiempo_jugado = diferencias[0:len(diferencias):2].sum()
    tiempo_no_jugado = diferencias[1:len(diferencias):2].sum()

    return round(tiempo_jugado/60, 0), round(tiempo_no_jugado/60, 0)