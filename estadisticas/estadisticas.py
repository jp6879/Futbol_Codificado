# Script que calula los laterales, goles y corners del partido
import math
from data_utils.data_handle import data_loader


def estadisticas_generales():
    """Función que devuelve las estadísticas del partido, goles, laterales y tiros de esquina

    Returns:
        goles_local (int): goles del equipo local
        goles_visitante (int): goles del equipo visitante
        laterales (int): laterales del partido
        corners (int): corners del partido
    """

    # Inicializamos las variables.
    goles_local = 0
    goles_visitante = 0
    laterales = 0
    corners = 0

    # Cargamos los datos.
    df_local, _ = data_loader()

    # Usamos las mismas dimensiones de la cancha.
    field_length = 105
    field_width = 68

    # Extramemos el total de frames.
    total_frames = len(df_local)

    for t in range(1, total_frames):
        # Extraemos el tiempo y la mitad en la que estamos.
        tiempo = df_local["Tiempo [s]"][t]
        periodo = df_local["Periodo"][t]

        # Extraemos las posiciones x e y de la pelota.
        x_pelota = df_local["Pelotax"][t] * field_length
        y_pelota = df_local["Pelotay"][t] * field_width


        # Lógica para contar los goles

        if periodo == 1:
            # Chequeamos que esté entre los postes de los arcos.
            if abs(y_pelota - field_width/2) < 7.35/2:
                x_rel = df_local["Pelotax"][t]
                x_rel_anterior = df_local["Pelotax"][t-1]
                x_rel_posterior = df_local["Pelotax"][t+1]
                # Chequeamos que la pelota haya pasado la línea de gol viendo si está adentro, si en el frame anterior estaba afuera y en el posterior está adentro o es NaN.
                if (x_rel > 1 and x_rel_anterior <= 1 and (x_rel_posterior > 1 or math.isnan(x_rel_posterior))):
                    # Chequeamos que haya sido valido el gol, porque puede haberse ido por arriba del arco o anularse.
                    # De la posición de la pelota en 50 cuadros (2 seg aprox) posteriores a esto los valores serán NaN porque sale la pelota de la cancha.
                    # Tomamos este nuevo DataFrame y vemos si cuando se reinicia el partido la pelota está en la mitad de la cancha.
                    # Si no quiere decir que si las condiciones anteriores se cumplieron esto no fue gol.
                    if math.isclose(df_local["Pelotax"][df_local["Pelotax"][t+50:].first_valid_index()], 0.5, abs_tol=0.2):
                        goles_local += 1
                # Misma lógica para los visitantes
                if (x_rel < 0 and x_rel_anterior >= 0 and (x_rel_posterior < 0 or math.isnan(x_rel_posterior))):
                    # Chequeamos que haya sido gol.
                    if math.isclose(df_local["Pelotax"][df_local["Pelotax"][t+50:].first_valid_index()], 0.5, abs_tol=0.2):
                        goles_visitante += 1

        # Mismo para el segundo tiempo
        elif periodo == 2:
            if abs(y_pelota - field_width/2) < 7.35/2:
                x_rel = df_local["Pelotax"][t]
                x_rel_anterior = df_local["Pelotax"][t-1]
                x_rel_posterior = df_local["Pelotax"][t+1]
                    # Hay un gol del equipo local que no se cuenta porque no aparece el frame cuando entra.
                if math.isclose(x_rel, 0, abs_tol = 0.004) and x_rel_anterior >= 0 and (x_rel_posterior > 1 or math.isnan(x_rel_posterior)):
                    # Chequeamos que haya sido gol.
                    if math.isclose(df_local["Pelotax"][df_local["Pelotax"][t+50:].first_valid_index()], 0.5, abs_tol=0.2):
                        goles_local += 1

                if x_rel > 1 and x_rel_anterior <= 1 and (x_rel_posterior or math.isnan(x_rel_posterior))> 1:
                    # Chequeamos que haya sido gol
                    if math.isclose(df_local["Pelotax"][df_local["Pelotax"][t+50:].first_valid_index()], 0.5, abs_tol=0.2):
                        goles_visitante += 1


        # Logica de laterales
        # Chequeamos que salió por los costados y no por las esquinas.
        if x_pelota > 0 and x_pelota < field_length:
            y_rel = df_local["Pelotay"][t]
            y_rel_anterior = df_local["Pelotay"][t-1]
            y_rel_posterior = df_local["Pelotay"][t+1]
            
            # Misma lógoca que para los golos chequeamos que haya cruzado las lineas de los laterales.
            if y_rel < 0  and y_rel_anterior >= 0 and (y_rel_posterior < 0 or math.isnan(y_rel_posterior)):
                # Chequemos si fue realmente lateral quedandonos con los 28 cuadros siguientes al segundo posterior (aprox 1 seg).
                # Luego vemos si hay algun NaN en esos cuadros, si lo hay es porque la pelota salió de la cancha.
                if (df_local["Pelotax"][t+2:t+30].isna().sum() != 0):
                    laterales += 1
            if y_rel > 1 and y_rel_anterior <= 1 and (y_rel_posterior > 1 or math.isnan(y_rel_posterior)):
                # if math.isnan(df_local["Pelotax"][t:t+5].any()):
                if(df_local["Pelotax"][t+2:t+30].isna().sum() != 0):
                    laterales += 1

        #Logica de los corners
        # La hacemos mas sencilla solo viendo si la pelota cruzó alguna de las lineas de fondo.
        if x_pelota < 0 and df_local["Pelotax"][t-1] >= 0: 
            # Si la pelota salió de la cancha a lo largo tomamos un DF con los valores de la pelota 25 cuadros para adelante.
            # Este deberia tener NaN hasta que se reinicie la posición de la pelota. Encontramos cuando se reinicia y si está en alguna de las 4 esquinas contamos un corner.
            x_posterior = df_local["Pelotax"][df_local["Pelotax"][t + 25:].first_valid_index()]
            y_posterior = df_local["Pelotay"][df_local["Pelotay"][t + 25:].first_valid_index()]
            if math.isclose(x_posterior, 0, abs_tol=0.2) and (math.isclose(y_posterior, 0, abs_tol=0.2) or math.isclose(y_posterior, 1, abs_tol=0.2)):
                corners += 1

        if x_pelota > field_length and df_local["Pelotax"][t-1] <= 1:
            x_posterior = df_local["Pelotax"][df_local["Pelotax"][t + 25:].first_valid_index()]
            y_posterior = df_local["Pelotay"][df_local["Pelotay"][t + 25:].first_valid_index()]
            if math.isclose(x_posterior, 1, abs_tol=0.2) and (math.isclose(y_posterior, 0, abs_tol=0.2) or math.isclose(y_posterior, 1, abs_tol=0.2)):
                corners += 1

    return goles_local, goles_visitante, laterales, corners