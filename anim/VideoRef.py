# Scripts para la animación de los datos
import numpy as np
import math
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from data_utils.data_handle import data_loader
from graficos.draw_field import draw_field
plt.ioff()

goles_local, goles_visitante, laterales, corners = 0, 0, 0, 0

def VideoRef(t1 : float, t2: float) -> None:
    """Función que muestra una animación del partido durante dos tiempos dados.

        Args:
            t1 (float): Tiempo inicial en minutos.
            t2 (float): Tiempo final en minutos.
        Returns:
            None
    """
    # Cargamos los datos
    df_local, df_visitante = data_loader()

    t1 = t1 * 60
    t2 = t2 * 60

    # Chequeamos que t1 < t2 y que ninguno de los dos supere el máximo tiempo del partido.
    try :
        if t1 > t2 or t1 > df_local["Tiempo [s]"].max() or t2 > df_local["Tiempo [s]"].max():
            raise ValueError("t1 debe ser menor que t2 y ambos deben ser tiempos validos del partido en minutos (0 a 95)")
        if t1 < 0:
            raise ValueError("t1 debe ser mayor que 0")
        if t2 < 0:
            raise ValueError("t2 debe ser mayor que 0")
    except ValueError as e:
        print(e)
        return
    
    # Tomamos los cuadros mas cercanos a estos dos tiempos para poder hacer la animación.
    cuadro_inicial = df_local["Cuadro"][abs(df_local["Tiempo [s]"] - t1).idxmin()]
    cuadro_final = df_local["Cuadro"][abs(df_local["Tiempo [s]"] - t2).idxmin()]
    
    frames = range(cuadro_inicial, cuadro_final)

    # Creamos la figura y el eje.
    fig, ax = draw_field()

    # Creamos los objetos que vamos a animar.
    scatter_locales = ax.scatter([],[], color="blue", s=70, edgecolors="white", label="Locales")
    scatter_visitantes = ax.scatter([],[], color="red", s=70, edgecolors="darkorange",label="Visitantes")
    scatter_pelota = ax.scatter([],[], color="black", s=20, edgecolors="white", label="Pelota")

    # Necesitamos el tamaño de la cancha para poder escalar los datos.
    field_length = 105
    field_width = 68
    
    # Creamos las listas de los nombres de los jugadores.
    locales = ["Jugador1", "Jugador2", "Jugador3", "Jugador4", "Jugador5", "Jugador6", "Jugador7", "Jugador8", "Jugador9", "Jugador10", "Jugador11", "Jugador12", "Jugador13", "Jugador14"]
    visitantes = ["Jugador15", "Jugador16", "Jugador17", "Jugador18", "Jugador19", "Jugador20", "Jugador21", "Jugador22", "Jugador23", "Jugador24", "Jugador25", "Jugador26", "Jugador27", "Jugador28"]

    # Creamos la función que se va a encargar de actualizar los datos en cada frame.
    def update(t):

        global goles_local, goles_visitante, laterales, corners

        # Extraemos el tiempo y la mitad en la que estamos.
        tiempo = df_local["Tiempo [s]"][t]
        periodo = df_local["Periodo"][t]

        # Extraemos las posiciones x e y de los jugadores locales y visitantes.
        x_locales = [df_local[lo + "x"][t] * field_length for lo in locales]
        y_locales = [df_local[lo + "y"][t] * field_width for lo in locales]

        x_visitantes = [df_visitante[visit + "x"][t] * field_length for visit in visitantes]
        y_visitantes = [df_visitante[visit + "y"][t] * field_width for visit in visitantes]

        # Extraemos las posiciones x e y de la pelota.
        x_pelota = df_local["Pelotax"][t] * field_length
        y_pelota = df_local["Pelotay"][t] * field_width

        # Actualizamos el título de la python football league.
        ax.set_title(f"$PyFL$ {round(tiempo/60, 2)}  "
                    r"$/Loc$"
                    f" {goles_local} / {goles_visitante} "
                    r"$Vis$/"
                    f" Laterales: {laterales} Corners: {corners}")

        # Actualizamos las posiciones de los jugadores y la pelota. Un poco magica esta función pero anda
        scatter_locales.set_offsets(np.array([[x_locales, y_locales]]).T)
        scatter_visitantes.set_offsets(np.array([[x_visitantes, y_visitantes]]).T)
        scatter_pelota.set_offsets(np.array([x_pelota, y_pelota]))

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

        # Avisamos de cambios en los equipos cuando un jugador cambia su posición en el campo de un valor numérico a NaN.
        for lo, visit in zip(locales, visitantes):
                if(math.isnan(df_local[lo + "x"][t-1]) and not math.isnan(df_local[lo + "x"][t])):
                    print("CAMBIO EN EL EQUIPO LOCAL")
                    print(lo, "entra al campo")
                if(not math.isnan(df_local[lo + "x"][t-1]) and math.isnan(df_local[lo + "x"][t])):
                    print(lo, "sale del campo") 
                
                if(math.isnan(df_visitante[visit + "x"][t-1]) and not math.isnan(df_visitante[visit + "x"][t])):
                    print("CAMBIO EN EL EQUIPO VISITANTE")
                    print(visit, "entra al campo")
                if(not math.isnan(df_visitante[visit + "x"][t-1]) and math.isnan(df_visitante[visit + "x"][t])):
                    print(visit, "sale del campo")


        return scatter_locales, scatter_visitantes, scatter_pelota
    
    anim = FuncAnimation(fig, update, frames=frames, repeat=False, interval = 0)
    plt.show()
