# LABORATORIO 5
# Daniela Navas
# Inteligencia Artificial - Ciclo 1 | 2025

# ----------------------------------------------------------------------
# Librerias 
# ----------------------------------------------------------------------
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# ======================================================================
#
# Task 1 - Graph-Search
#
# ======================================================================

# ======================================================================
# Task 1.1 - Discretización de la imagen
# ======================================================================

# ----------------------------------------------------------------------
# FUNCIÓN PARA DEFINIR COLOR
# Los colores en la imagen (especialmente aquellos que no son blanco 
# y negro) no siempre son del código RGB exacto, por ello se define una
# rango aceptable.
# ----------------------------------------------------------------------
def def_color(r, g, b, color, tolerancia):
    """
    Param:
        r (int): Componente rojo del color.
        g (int): Componente verde del color.
        b (int): Componente azul del color.
        color (tuple): Tupla que contiene el color de referencia (r_ref, g_ref, b_ref).
        tolerancia (int): Valor que define el rango de tolerancia para la comparación.

    Return:
        bool: True si el color está dentro del rango de tolerancia, False en caso contrario.
    """
    r_ref, g_ref, b_ref = color # Verifica si un color está dentro de la tolerancia de otro
    return (abs(r - r_ref) <= tolerancia and
            abs(g - g_ref) <= tolerancia and
            abs(b - b_ref) <= tolerancia)

# ----------------------------------------------------------------------
# IMAGEN A MATRIZ
# Procesa una imagen, reduce su tamaño y convierte cada píxel en un 
# valor correspondiente a su color en la matriz:
# - Blanco -> 0 (Camino libre)
# - Negro -> 1 (Pared)
# - Verde -> 2 (Meta)
# - Rojo -> 3 (Inicio)
# ----------------------------------------------------------------------
def imagen_a_matriz(ruta_imagen, factor_escala, tolerancia):
    """
    Param:
        ruta_imagen (str): Ruta del archivo de imagen a procesar.
        factor_escala (int): Factor de escala para redimensionar la imagen.
        tolerancia (int): Tolerancia para la comparación de colores.

    Return:
        numpy.ndarray: Matriz con valores enteros que representan los colores procesados de la imagen.
    """
    img = Image.open(ruta_imagen).convert("RGB")                       # Carga la imagen y la convierte a formato RGB
    ancho, alto = img.size                                             # Obtiene las dimensiones originales de la imagen
    img = img.resize((ancho // factor_escala, alto // factor_escala))  # Redimensiona la imagen según el factor de escala
    pixeles = np.array(img)                                            # Convierte la imagen en un array de píxeles RGB
    matriz = np.zeros((pixeles.shape[0], pixeles.shape[1]), dtype=int) # Inicializa una matriz de ceros del mismo tamaño

    # Recorre cada píxel de la imagen y asigna un valor a la matriz dependiendo del color
    for i in range(pixeles.shape[0]):
        for j in range(pixeles.shape[1]):
            r, g, b = pixeles[i, j] # Obtiene los valores RGB de cada píxel

            # Compara el color de cada píxel con los colores definidos
            if def_color(r, g, b, (255, 255, 255), tolerancia):  # Blanco
                matriz[i, j] = 0                                 # Camino libre
            elif def_color(r, g, b, (0, 0, 0), tolerancia):  # Negro
                matriz[i, j] = 1                             # Pared
            elif def_color(r, g, b, (0, 255, 0), tolerancia):  # Verde
                matriz[i, j] = 2                               # Meta
            elif def_color(r, g, b, (255, 0, 0), tolerancia):  # Rojo
                matriz[i, j] = 3                               # Inicio

    return matriz # Devuelve la matriz resultante

# Para evitar errores se obtiene la ruta del directorio donde está guardado el script
# directorio_actual = os.path.dirname(os.path.abspath(__file__))
# ruta_imagen = os.path.join(directorio_actual, "PruebaLab1.bmp") # Concatenar con la ruta de la imagen

# ABRIR IMAGEN DESDE EL EXPLORADOR DE ARCHIVOS 

Tk().withdraw() # Evitar que se abra una ventana vacía de tkinter
ruta_imagen = askopenfilename(title="Seleccionar imagen", filetypes=[("Archivos de imagen", "*.bmp;*.png")]) # Abrir el cuadro de diálogo para seleccionar la imagen

# Si se selecciona una imagen, se guarda la ruta
if ruta_imagen:
    print(f"Ruta de la imagen seleccionada: {ruta_imagen}")
else:
    print("No se seleccionó ninguna imagen.")

# Convertir la imagen en matriz
escala = 10       # Definir escala
tolerancia = 30   # Definir tolerancia
matriz_lab = imagen_a_matriz(ruta_imagen, escala, tolerancia)

# Configurar para imprimir toda la matriz
np.set_printoptions(threshold=np.inf)

# Mostrar la matriz
print(matriz_lab)

# Visualizar la matriz con colores
plt.imshow(matriz_lab, cmap="nipy_spectral")
plt.colorbar()
plt.title("Matriz del Laberinto")
plt.show()

# ======================================================================
# Task 1.2 - Framework de Problemas
# ======================================================================