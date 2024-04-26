# Scripts para el limpiado de los datos
import os

import pandas as pd
import numpy as np
from typing import Tuple

def data_loader() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Función que carga los datos de los DataFrames de los equipos locales y visitantes.

        Returns:
            df_local (pd.DataFrame): DataFrame con los datos del equipo local mas datos extra como periodo, cuadro, tiempo y pelota.
            df_visitante (pd.DataFrame): DataFrame con los datos del equipo visitante mas datos extra como periodo, cuadro, tiempo y pelota.

        Carga los datos de los DataFrames de los equipos locales y visitantes, y los retorna para poder trabajar con ellos.
    """

    # Cargamos los datos de los DataFrames de los equipos locales y visitantes.
    df_local = pd.read_csv('../data/Local.csv')
    df_visitante = pd.read_csv('/Visitante.csv')

    # df_local = pd.read_csv(os.path.join(r'C:\Users\Propietario\Desktop\ib\5-Maestría\Intro Python\Ejercicios\Final\Futbol_Codificado\Futbol_Codificado\data\Local.csv'), low_memory=False)
    # df_visitante = pd.read_csv(os.path.join(r'C:\Users\Propietario\Desktop\ib\5-Maestría\Intro Python\Ejercicios\Final\Futbol_Codificado\Futbol_Codificado\data\Visitante.csv'), low_memory=False)

    # Limpiamos las primeras filas del DataFrame y renombramos las columnas.
    df_local, df_visitante = clean_data(df_local, df_visitante)
    
    return df_local, df_visitante


def clean_data(df_local : pd.DataFrame, df_visitante : pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Función que limplia los datos de los DataFrames para poder tener un manejo adecuado

        Args:
            df_local (pd.DataFrame): DataFrame con los datos del equipo local mas datos extra como periodo, cuadro, tiempo y pelota.
            df_visitante (pd.DataFrame): DataFrame con los datos del equipo visitante mas datos extra como periodo, cuadro, tiempo y pelota.

        Returns:
            df_local (pd.DataFrame): DataFrame con los datos del equipo local mas datos extra como periodo, cuadro, tiempo y pelota.
            df_visitante (pd.DataFrame): DataFrame con los datos del equipo visitante mas datos extra como periodo, cuadro, tiempo y pelota.

        De ambos DataFrames se cambian los nombres de las columnas adecuadamente se cambian todos los datos a datos numéricos para poder trabajarlos,
        se tiran las filas aquellas en las que la pelota tiene una posición NaN y se resetean los índices de ambos DataFrames en cada cambio realizado.
    """
    # Obtenemos el nombre de las columnas para cada DataFrame.
    columns_local = df_local.iloc[1,:].values
    columns_visitante = df_visitante.iloc[1,:].values

    # Cambiamos aquellas columnas con valores NaN por 0.0, estos quedan convertidos en strings porque el DataFrame trata de no mezclar tipos.
    columns_local = np.array(list(map(np.nan_to_num, columns_local)))
    columns_visitante = np.array(list(map(np.nan_to_num, columns_visitante)))

    # Los que quedaron como 0.0 los cambiamos por la columna anterior + 'y' que es realmente lo que significa estas columnas.
    for i in range(len(columns_local)):
        if columns_local[i] == '0.0':
            columns_local[i] = columns_local[i-1] + 'y'
            columns_local[i-1] = columns_local[i-1] + 'x'
        if columns_visitante[i] == '0.0':
            columns_visitante[i] = columns_visitante[i-1] + 'y'
            columns_visitante[i-1] = columns_visitante[i-1] + 'x'

    # Tiramos las primeras dos filas que no tienen datos relevantes para ambos DataFrames.
    df_local = df_local.drop([0,1])
    df_local.columns = columns_local

    df_visitante = df_visitante.drop([0,1])
    df_visitante.columns = columns_visitante

    # Cambiamos todos los valores a valores numéricos para poder trabajar.
    df_local = df_local.apply(pd.to_numeric)
    df_visitante = df_visitante.apply(pd.to_numeric)

    # Reseteamos los indices después de todos los cambios que realizamos.
    df_local = df_local.reset_index(drop=True)
    df_visitante = df_visitante.reset_index(drop=True)

    return df_local, df_visitante

# Función auxiliar max min scale para normalizar los datos.
def max_min_scale(arr : np.array) -> np.array:
    """Función que normaliza los datos de un array.
        Args:
            arr (np.array): array de datos a normalizar.

        Returns:
            (np.array): array de datos normalizados.

        Normaliza los datos de un array para que estén en el rango [0,1]."""
    new_min, new_max = 0, 1
    old_min, old_max = arr.min(), arr.max()
    return (arr - old_min) / (old_max - old_min) * (new_max - new_min) + new_min