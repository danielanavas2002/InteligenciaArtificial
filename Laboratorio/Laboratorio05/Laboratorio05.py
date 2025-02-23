# LABORATORIO 5
# Daniela Navas
# Inteligencia Artificial - Ciclo 1 | 2025

# ----------------------------------------------------------------------
# Librerias 
# ----------------------------------------------------------------------
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from abc import ABC, abstractmethod
from collections import deque
import heapq

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

# IMAGEN CON RUTA DEL DIRECTORIO (Solo se uso para pruebas iniciales)
# Para evitar errores se obtiene la ruta del directorio donde está guardado el script
# directorio_actual = os.path.dirname(os.path.abspath(__file__))
# ruta_imagen = os.path.join(directorio_actual, "PruebaLab1.bmp") # Concatenar con la ruta de la imagen

# ABRIR IMAGEN DESDE EL EXPLORADOR DE ARCHIVOS ----------------------------------------------------------
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

# Visualizar Matriz (Solo para pruebas)
# np.set_printoptions(threshold=np.inf) # Configurar para imprimir toda la matriz
# print(matriz_lab) # Mostrar la matriz

# Mostrar Matriz extraída de la imagen
colors = ['white', 'black', 'green', 'red'] 
cmap_1 = ListedColormap(colors)
plt.imshow(matriz_lab, cmap=cmap_1)
plt.title("Matriz del Laberinto")
plt.show()

# ======================================================================
# Task 1.2 - Framework de Problemas
# ======================================================================
"""
Clase Problema
Interfaz genérica que define las funciones necesarias para resolver un 
problema de búsqueda. La idea es que esta clase establezca los métodos 
clave que todos los problemas deben implementa
"""
class Problema(ABC):
    def __init__(self, matriz):
        self.matriz = matriz
        self.filas = len(matriz)
        self.columnas = len(matriz[0])
        self.inicio = self.encontrar_posicion(3)  # Rojo (3 en Matriz) es Inicio
        self.meta = self.encontrar_posicion(2)    # Verde (2 en Matriz) es la Meta

    def encontrar_posicion(self, valor):
        """
        Encuentra la posición de un valor en la matriz.
        """
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.matriz[i][j] == valor:
                    return (i, j)
        return None

    # Definir métodos que deben ser implementados:
    @abstractmethod
    def actions(self, estado):
        pass

    @abstractmethod
    def stepCost(self, estado, accion, nuevo_estado):
        pass

    @abstractmethod
    def goalTest(self, estado):
        pass

    @abstractmethod
    def h(self, estado):
        pass

"""
Clase Laberinto
Subclase de Problema 
Implementa las funciones necesarias para representar y resolver el problema 
específico del laberinto. Aquí es donde se define cómo interactuar con la 
estructura del laberinto y cómo generar las acciones posibles, calcular costos,
y aplicar las heurísticas.
"""
class Laberinto(Problema):
    def actions(self, estado):
        """
        Return:
         - Acciones posibles desde el estado dado.
            Las acciones posibles son: mover arriba, abajo, izquierda, derecha.
        """
        acciones = []
        x, y = estado
        if x > 0 and self.matriz[x - 1][y] != 1:  # No es pared
            acciones.append('arriba')
        if x < self.filas - 1 and self.matriz[x + 1][y] != 1:  # No es pared
            acciones.append('abajo')
        if y > 0 and self.matriz[x][y - 1] != 1:  # No es pared
            acciones.append('izquierda')
        if y < self.columnas - 1 and self.matriz[x][y + 1] != 1:  # No es pared
            acciones.append('derecha')
        return acciones

    def stepCost(self, estado, accion, nuevo_estado):
        """
        Return:
        Costo de tomar una acción desde el estado dado.
        Se *asume* que todas las acciones tienen un costo de 1
        """
        return 1

    def goalTest(self, estado):
        """
        Verifica si el estado actual es la meta
        """
        return estado == self.meta

    def h(self, estado):
        """
        Función heurística: distancia de Manhattan desde el estado actual hasta la meta
        """
        x, y = estado
        x_meta, y_meta = self.meta
        return abs(x - x_meta) + abs(y - y_meta)

# Para pruebas: 
# problema = Laberinto(matriz_lab) # Crear el problema del laberinto
# acciones_posibles = problema.actions(problema.inicio) # Obtener acciones posibles desde el estado de inicio
# print(f"Acciones posibles desde el inicio: {acciones_posibles}")
# es_meta = problema.goalTest(problema.inicio) # Verificar si hemos alcanzado la meta
# print(f"¿Hemos llegado a la meta? {es_meta}")

# ======================================================================
# Task 1.3 - Graph-Search
# ======================================================================
# ----------------------------------------------------------------------
# GRAPH-SEARCH
# Función genérica para realizar una búsqueda en un problema
# ----------------------------------------------------------------------
def graphSearch(problema, estrategia="BFS"):
    """
    Params:
    - problema: Instancia de la clase Problema.
    - estrategia: El tipo de búsqueda ('BFS', 'DFS', 'A*').

    Return:
    - Un camino hacia la meta si se encuentra, de lo contrario, None.
    """
    # Estado inicial
    estado_inicial = problema.inicio
    meta = problema.meta

    # Inicializar las estructuras de datos según la estrategia
    if estrategia == "BFS":
        frontera = deque([estado_inicial])             # FIFO (BFS)
        visitados = set()
    elif estrategia == "DFS":
        frontera = [estado_inicial]                    # LIFO (DFS)
        visitados = set()
    elif estrategia == "A*":
        frontera = []                                  # Cola de prioridad (A*)
        heapq.heappush(frontera, (0, estado_inicial))  # (costo + heurística, estado)
        visitados = set()
    else:
        raise ValueError(f"Estrategia '{estrategia}' no reconocida.")

    # Diccionario para seguir el camino
    padre = {estado_inicial: None}

    while frontera:
        if estrategia == "BFS":
            estado_actual = frontera.popleft()          # Explorar el primero (BFS)
        elif estrategia == "DFS":
            estado_actual = frontera.pop()              # Explorar el último (DFS)
        elif estrategia == "A*":
            _, estado_actual = heapq.heappop(frontera)  # Explorar el de menor costo estimado

        # Verificar si se llego a la meta
        if problema.goalTest(estado_actual):
            # Reconstruir el camino hacia la meta
            camino = []
            while estado_actual is not None:
                camino.append(estado_actual)
                estado_actual = padre[estado_actual]
            return camino[::-1]  # Invertir el camino para obtener la secuencia de inicio a meta

        # Marcar como visitado
        visitados.add(estado_actual)

        # Explorar los vecinos
        for accion in problema.actions(estado_actual):
            nuevo_estado = apply_action(estado_actual, accion)  # Función auxiliar para aplicar la acción
            if nuevo_estado not in visitados:
                # Para A*, añadir el costo + heurística
                if estrategia == "A*":
                    costo = problema.stepCost(estado_actual, accion, nuevo_estado)
                    heuristica = problema.h(nuevo_estado)
                    heapq.heappush(frontera, (costo + heuristica, nuevo_estado))

                # Para BFS y DFS, añadir el estado a la frontera
                if estrategia != "A*":
                    frontera.append(nuevo_estado)

                # Agregar el estado al diccionario de padres
                padre[nuevo_estado] = estado_actual

    return None  # Si no se encuentra un camino

# ----------------------------------------------------------------------
# APPLY_ACTION
# Función auxiliar para aplicar la acción sobre el estado
# ----------------------------------------------------------------------
def apply_action(estado, accion):
    # Aplicar las acciones dependiendo de cómo se represente el estado, 
    # en el caso de un laberinto representado por coordenadas (x, y), 
    # las acciones son:
    x, y = estado
    if accion == "arriba":
        return (x - 1, y)
    elif accion == "abajo":
        return (x + 1, y)
    elif accion == "izquierda":
        return (x, y - 1)
    elif accion == "derecha":
        return (x, y + 1)
    return estado

# ----------------------------------------------------------------------
# DISTANCIA_MANHATTAN
# Calcula la distancia de Manhattan entre el estado actual y la meta
# ----------------------------------------------------------------------
def distancia_manhattan(estado, meta):
    x1, y1 = estado
    x2, y2 = meta
    return abs(x1 - x2) + abs(y1 - y2)

# ----------------------------------------------------------------------
# DISTANCIA_EUCLIDIANA
# Calcula la distancia Euclidiana entre el estado actual y la meta
# ----------------------------------------------------------------------
def distancia_euclidiana(estado, meta):
    x1, y1 = estado
    x2, y2 = meta
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

# Para pruebas:
# Crear el problema del laberinto

matriz_lab = [
    [3, 0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 2, 0]
]

problema = Laberinto(matriz_lab) # Crear la instancia del laberinto

print("Calculando camino BFS...")
camino_bfs = graphSearch(problema, estrategia="BFS") # Realizar una búsqueda BFS
print(f"Camino BFS: {camino_bfs}")
print("-----------------------------------------------------------------------------------------")

print("Calculando camino DFS...")
camino_dfs = graphSearch(problema, estrategia="DFS")
print(f"Camino DFS: {camino_dfs}")
print("-----------------------------------------------------------------------------------------")

print("Calculando camino A*...")
problema.h = lambda estado: distancia_manhattan(estado, problema.meta) # Realizar una búsqueda A* con la heurística de Manhattan
camino_a_star = graphSearch(problema, estrategia="A*")
print(f"Camino A* (Manhattan): {camino_a_star}")
print("-----------------------------------------------------------------------------------------")

# ======================================================================
# Task 1.4 - Construcción de Salida
# ======================================================================
# ----------------------------------------------------------------------
# GRAFICAR_CAMINO
# Muestra la matriz del laberinto (extraido previamente) con el camino 
# resaltado en color rosado
# ----------------------------------------------------------------------
def graficar_camino(matriz, camino, tittle):
    """
    Param:
        matriz (numpy.ndarray): La matriz representando el laberinto.
        camino (list): Una lista de tuplas (x, y) representando el camino encontrado.
    """
    # Asegurarse de que la matriz sea un ndarray
    matriz_camino = np.array(matriz)  # Convertir la matriz a numpy.ndarray
    
    # Marcar el camino con un valor de 4 (rosado)
    for (x, y) in camino:
        matriz_camino[x, y] = 4

    # Definir el colormap personalizado
    colores = ['white', 'black', 'green', 'red', 'magenta']  # Blanco, negro, verde, rojo, magenta
    cmap = ListedColormap(colores)

    # Mostrar la matriz con el camino resaltado
    plt.imshow(matriz_camino, cmap=cmap, interpolation="nearest")
    plt.title(tittle)
    plt.xticks([])  # Elimina los valores del eje x
    plt.yticks([])  # Elimina los valores del eje y
    plt.show()

# Con BFS 
if camino_bfs:
    tittle = "Laberito Resuelto | BFS"
    graficar_camino(matriz_lab, camino_bfs, tittle)

# Con BFS 
if camino_dfs:
    tittle = "Laberito Resuelto | DFS"
    graficar_camino(matriz_lab, camino_dfs, tittle)

# A*
if camino_a_star:
    tittle = "Laberito Resuelto | A*"
    graficar_camino(matriz_lab, camino_a_star, tittle)
