# LABORATORIO 5
# Daniela Navas
# Inteligencia Artificial - Ciclo 1 | 2025

# ----------------------------------------------------------------------
# Task 1 - Graph-Search
# ----------------------------------------------------------------------

import cv2
import numpy as np

def imagen_a_matriz(ruta_imagen, grid_size=20):
    """
    - 0: Pared (negro)
    - 1: Camino libre (blanco)
    - 2: Meta (verde)
    - 3: Punto de inicio (rojo)
    """
    # Cargar la imagen
    imagen = cv2.imread(ruta_imagen)

    # Convertir a espacio de color HSV para detección de colores
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    # Definir rangos de colores en HSV
    colores = {
        "blanco": ([0, 0, 200], [180, 30, 255]),  # Caminos libres
        "negro": ([0, 0, 0], [180, 255, 30]),  # Paredes
        "rojo1": ([0, 120, 70], [10, 255, 255]),  # Rojo (inicio)
        "rojo2": ([170, 120, 70], [180, 255, 255]),
        "verde": ([40, 40, 40], [80, 255, 255])  # Metas
    }

    # Obtener dimensiones y tamaño de cada celda
    alto, ancho, _ = imagen.shape
    celda_alto = alto // grid_size
    celda_ancho = ancho // grid_size

    # Inicializar matriz del laberinto
    matriz = np.zeros((grid_size, grid_size), dtype=int)

    for i in range(grid_size):
        for j in range(grid_size):
            # Obtener la región de la celda
            y_ini, y_fin = i * celda_alto, (i + 1) * celda_alto
            x_ini, x_fin = j * celda_ancho, (j + 1) * celda_ancho
            celda = hsv[y_ini:y_fin, x_ini:x_fin]

            # Contar píxeles de cada color en la celda
            contadores = {
                "blanco": np.sum(cv2.inRange(celda, np.array(colores["blanco"][0]), np.array(colores["blanco"][1]))),
                "negro": np.sum(cv2.inRange(celda, np.array(colores["negro"][0]), np.array(colores["negro"][1]))),
                "rojo": np.sum(cv2.inRange(celda, np.array(colores["rojo1"][0]), np.array(colores["rojo1"][1]))) +
                        np.sum(cv2.inRange(celda, np.array(colores["rojo2"][0]), np.array(colores["rojo2"][1]))),
                "verde": np.sum(cv2.inRange(celda, np.array(colores["verde"][0]), np.array(colores["verde"][1]))),
            }

            # Determinar el color dominante
            color_dominante = max(contadores, key=contadores.get)

            # Asignar el valor en la matriz
            if color_dominante == "negro":
                matriz[i, j] = 0  # Pared
            elif color_dominante == "blanco":
                matriz[i, j] = 1  # Camino libre
            elif color_dominante == "rojo":
                matriz[i, j] = 3  # Punto de inicio
            elif color_dominante == "verde":
                matriz[i, j] = 2  # Meta

    return matriz

# Ruta de la imagen
ruta_imagen = "PruebaLab1.bmp"  

# Convertir la imagen a matriz
matriz_laberinto = imagen_a_matriz(ruta_imagen)

# Mostrar la matriz resultante
print(matriz_laberinto)
