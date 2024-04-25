from matplotlib import pyplot as plt
from anim.VideoRef import VideoRef
from data_utils.data_handle import data_loader
from estadisticas.masveloz import encuentra_mas_veloz
from estadisticas.tiemponeto import tiempo_neto
from estadisticas.estadisticas import estadisticas_generales
from graficos.heatmap import heatmap
from graficos.draw_field import draw_field

if __name__ == "__main__":
    titulo = "Graficamos el campo de juego"
    n = int(60-len(titulo)//2)
    print("*"*n + titulo + "*"*n)
    fig, ax = draw_field()
    plt.show()

    print("")

    titulo = "Ingrese dos tiempos en minutos para graficar una animación del partido"
    n = int(60-len(titulo)//2)
    print("*"*n + titulo + "*"*n)
    tiempo_inicial = float(input("Tiempo inicial: "))
    tiempo_final = float(input("Tiempo final: "))
    VideoRef(tiempo_inicial, tiempo_final)
    
    print("")

    titulo = "Graficamos el mapa de calor de un jugador"
    n = int(60-len(titulo)//2)
    print("*"*n + titulo + "*"*n)
    print("Ingrese el número de un jugador entre 1 y 28")
    try:
        int_jugador = int(input("Número de jugador: "))
        jugador = "Jugador" + str(int_jugador)
        heatmap(jugador)
    except ValueError:
        print("Ingrese un número válido")
    
    print("")

    titulo = "Calculamos el jugador más veloz del partido"
    n = int(60-len(titulo)//2)
    print("*"*n + titulo + "*"*n)
    velocidad, jugador_mas_veloz = encuentra_mas_veloz()
    print(f"El jugador más veloz del partido fue {jugador_mas_veloz} con una velocidad media de {velocidad} m/s")

    print("")

    titulo = "Calculamos las estadísticas generales del partido"
    n = int(60-len(titulo)//2)
    print("*"*n + titulo + "*"*n)
    goles_local, goles_visitante, laterales, corners = estadisticas_generales()
    print(f"El equipo local hizo {goles_local} goles, el equipo visitante hizo {goles_visitante} goles, se cobraron {laterales} laterales y {corners} corners")

    print("")

    titulo = "Calculamos el tiempo neto jugado en el partido"
    n = int(60-len(titulo)//2)
    print("*"*n + titulo + "*"*n)
    tiempo_jugado, tiempo_no_jugado = tiempo_neto()
    print(f"El tiempo neto jugado en el partido fue de {tiempo_jugado} minutos y el tiempo no jugado fue de {tiempo_no_jugado} minutos")
