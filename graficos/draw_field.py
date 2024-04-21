from matplotlib import pyplot as plt
from matplotlib import patches

def draw_field() -> tuple[plt.Figure, plt.Axes]:
    """Función que grafíca una cancha de futbol según las dimensiones de la FIFA y devuelve los objetos fig y ax de matplotlib.
        Args:
            Ninguno
        Returns:
            fig: figura de matplotlib
            ax: eje de la figura
    """

    # Creamos la figura sobre la cual vamos a dibujar la cancha.
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_axis_off() # Sacamos los ejes para que no se vean en la animación.

    # Dimensiones en metros según la FIFA de la cancha.
    field_length = 105
    field_width = 68
    
    # Agregamos el pasto afuera de la cancha.
    grassed_length = field_length + 8
    grassed_width = field_width + 8

    # Grassed area como le llama la FIFA.
    grassed_area = patches.Rectangle((-4,-4), grassed_length, grassed_width, facecolor='darkgreen', capstyle='round')
    ax.add_patch(grassed_area)

    # Campo de juego (rectángulo).
    field = patches.Rectangle((0,0), field_length, field_width, linewidth=1, edgecolor='white', facecolor='forestgreen', capstyle='round')
    ax.add_patch(field)
    
    # Circulo y marca central.
    radius_cc = 9.15
    
    center_circle = plt.Circle((field_length/2, field_width/2), radius_cc, color="white", fill=False)
    center_mark = plt.Circle((field_length/2, field_width/2), 0.5, color="white", fill=True)
    ax.add_patch(center_circle)
    ax.add_patch(center_mark)
    
    # Mitad de cancha.
    ax.add_patch(patches.Rectangle((field_length/2, 0), 0, field_width, edgecolor="white", facecolor="none"))

    # Tamaño de area de penal.
    penalty_area_length = 16.5
    penalty_area_width = 40.32

    ax.add_patch(patches.Rectangle((0, (field_width-penalty_area_width)/2), penalty_area_length, penalty_area_width, edgecolor="white", facecolor="none"))
    ax.add_patch(patches.Rectangle((field_length-penalty_area_length, (field_width-penalty_area_width)/2), penalty_area_length, penalty_area_width, edgecolor="white", facecolor="none"))

    # Tamaño de area chica.
    small_area_lenght = 5.5
    small_area_width = 18.32

    ax.add_patch(patches.Rectangle((0, (field_width-small_area_width)/2), small_area_lenght, small_area_width, edgecolor="white", facecolor="none"))
    ax.add_patch(patches.Rectangle((field_length-small_area_lenght, (field_width-small_area_width)/2), small_area_lenght, small_area_width, edgecolor="white", facecolor="none"))

    # Puntos penal.
    penalty_mark = plt.Circle((11,field_width/2), 0.4, color="white", fill=True)
    penalty_mark_2 = plt.Circle((field_length-11,field_width/2), 0.4, color="white", fill=True)
    ax.add_patch(penalty_mark)
    ax.add_patch(penalty_mark_2)

    # Semi circulos de area.
    diameter_sc = 9.15*2
    ax.add_patch(patches.Arc((11,field_width/2), diameter_sc, diameter_sc, angle=0, theta1=308, theta2=52, color="white"))
    ax.add_patch(patches.Arc((field_length - 11 ,field_width/2), diameter_sc, diameter_sc, angle=0, theta1=127, theta2=233, color="white"))

    # Arcos de esquina.
    ax.add_patch(patches.Arc((0,0), 2, 2, angle=0, theta1=0, theta2=90, color = "white"))
    ax.add_patch(patches.Arc((field_length,0), 2, 2, angle=0, theta1=90, theta2=180, color = "white"))
    ax.add_patch(patches.Arc((0,field_width), 2, 2, angle=0, theta1=270, theta2=0, color = "white"))
    ax.add_patch(patches.Arc((field_length,field_width), 2, 2, angle=0, theta1=180, theta2=-90, color = "white"))

    # Arcos.
    arc_length = 7.32
    arc_width = 2.5 # Solo para visualización.
    ax.add_patch(patches.Rectangle((-arc_width, field_width/2 - arc_length/2), arc_width, arc_length, edgecolor="white", facecolor="none")) # Arco izquierdo
    ax.add_patch(patches.Rectangle((field_length, field_width/2 - arc_length/2), arc_width, arc_length, edgecolor="white", facecolor="none"))
    
    # Escalar las dimensiones para una mejor visualización.
    ax.set_xlim(-4, field_length+4)
    ax.set_ylim(-4, field_width+4)
    ax.set_aspect('equal') # Para que los ejes tengan la misma escala.
    ax.invert_yaxis() # Para machear los datos con la cancha, esquina superior izquierda es el origen.

    return fig, ax