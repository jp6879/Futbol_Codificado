# Futbol Codificado

> Programa que lee datos de arhivos con los datos de un partido de fútbol y provee distintas funcionalidades.

* Los archivos Local.csv y Visitante.csv contienen los datos obtenidos para el movimiento de todos los jugadores y la pelota, para el equipo local y el equipo visitante, respectivamente.
* La primera columna corresponde al período (primero o segundo) del partido. La segunda columna es el número de cuadro (frame) en el que están tomados los datos, que se corresponde con el tiempo en segundos definido en la tercer columna. Las siguientes columnas corresponden a las posiciones x e y de cada jugador en el campo de juego. Finalmente, las últimas dos columnas corresponden a las posiciones x e y del balón.

* Las coordenadas x e y están obtenidas en valores relativos entre 0 y 1, siendo la posición (0,0) la del corner superior izquierdo, y la (1,1) la del corner inferior derecho. Las dimensiones establecidas por la FIFA corresponden a un campo de juego de 105 m de largo por 68 m de ancho.

## Funcionalidades

  1. Se crea el grafico de la cancha de futbol que representa adecuadamente las dimensiones reales del mismo.
  2. VideoRef: Dados dos tiempos $t_1$ y $t_2$, crea una animación del juego entre esos dos tiempos, representada sobre el campo de juego graficado en 1. La animación distingue entre los dos equipos y la pelota.
  3. Avisa de los cambios de jugadores que se producen en el partido.
  3. Dado un jugador a elección, se grafica el mapa de calor del mismo a lo largo del partido.
  4. Se encuentra el jugador mas rápido del partido y su velocidad promedio.
  5. Se determinan cuantos goles, corners y laterales se cobraron
  6. Se encuentra el tieempo de juego neto (definido como el tiempo durante el cual el balón está dentro del campo de juego)
