# LIBRERIAS
import numpy as np
import pygame
import sys
import math
import random
import tkinter as tk
import matplotlib.pyplot as plt

# Inicializar Pygame
pygame.init()

# Definir constantes para ejecución de juego
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)

# Definir colores para juego
SKYBLUE = (135, 206, 235)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Definir variables para flujo de juego
PLAYER = 0
AI = 1
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4

# Crear el tablero del juego como una matriz de ceros
def create_board():
    """
    Crea un tablero de Conecta 4 representado como una matriz de ceros.
    Filas: ROW_COUNT, Columnas: COLUMN_COUNT.
    """
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# Colocar una ficha en el tablero
def drop_piece(board, row, col, piece):
    """
    Coloca una ficha en el tablero en la posición especificada.
    
    Param:
    - board: La matriz que representa el tablero.
    - row: La fila donde se colocará la ficha.
    - col: La columna donde se colocará la ficha.
    - piece: El valor de la ficha (1 o 2) correspondiente al jugador.
    """
    board[row][col] = piece

# Verificar si una columna está disponible para jugar
def is_valid_location(board, col):
    """
    Verifica si una columna tiene espacio disponible para colocar una ficha.
    
    Param:
    - board: La matriz que representa el tablero.
    - col: La columna a verificar.

    Return:
    - True si hay espacio en la columna, False si está llena.
    """
    return board[ROW_COUNT-1][col] == 0

# Encontrar la siguiente fila vacía en una columna
def get_next_open_row(board, col):
    """
    Busca la primera fila vacía en la columna seleccionada.
    
    Param:
    - board: La matriz que representa el tablero.
    - col: La columna en la que se busca espacio.

    Return:
    - El índice de la fila vacía más baja en la columna.
    """
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Imprimir el tablero (para depuración)
def print_board(board):
    """
    Imprime el tablero en la consola con las filas en el orden correcto.
    
    Param:
    - board: La matriz que representa el tablero de juego.
    """
    print(np.flip(board, 0)) # Se usa np.flip(board, 0) para mostrar la matriz con la fila superior en la parte superior.

# Verificar si un jugador ha ganado la partida
def winning_move(board, piece):
    """
    Comprueba si el jugador actual ha ganado con su última jugada.
    
    Param:
    - board: La matriz que representa el tablero de juego.
    - piece: La ficha del jugador (1 o 2).
    
    Return:
    - True si hay una combinación ganadora, False en caso contrario.

    Condiciones de victoria:
    - Cuatro fichas alineadas horizontalmente.
    - Cuatro fichas alineadas verticalmente.
    - Cuatro fichas alineadas en una diagonal con pendiente positiva (\).
    - Cuatro fichas alineadas en una diagonal con pendiente negativa (/).
    """

    # Verificar combinaciones horizontales
    for c in range(COLUMN_COUNT - 3):  # Solo revisa hasta la cuarta última columna
        for r in range(ROW_COUNT):  # Recorre todas las filas
            if (board[r][c] == piece and board[r][c+1] == piece and 
                board[r][c+2] == piece and board[r][c+3] == piece):
                return True

    # Verificar combinaciones verticales
    for c in range(COLUMN_COUNT):  # Recorre todas las columnas
        for r in range(ROW_COUNT - 3):  # Solo revisa hasta la cuarta última fila
            if (board[r][c] == piece and board[r+1][c] == piece and 
                board[r+2][c] == piece and board[r+3][c] == piece):
                return True

    # Verificar combinaciones diagonales con pendiente positiva (\)
    for c in range(COLUMN_COUNT - 3):  # Evita salir del rango de columnas
        for r in range(ROW_COUNT - 3):  # Evita salir del rango de filas
            if (board[r][c] == piece and board[r+1][c+1] == piece and 
                board[r+2][c+2] == piece and board[r+3][c+3] == piece):
                return True

    # Verificar combinaciones diagonales con pendiente negativa (/)
    for c in range(COLUMN_COUNT - 3):  # Evita salir del rango de columnas
        for r in range(3, ROW_COUNT):  # Empieza en la cuarta fila y avanza hacia abajo
            if (board[r][c] == piece and board[r-1][c+1] == piece and 
                board[r-2][c+2] == piece and board[r-3][c+3] == piece):
                return True

    return False  # Si no encuentra ninguna combinación ganadora

# Evaluar una ventana de cuatro posiciones para determinar la puntuación de la IA
def evaluate_window(window, piece):
    """
    Evalúa una ventana (subsección) de cuatro posiciones en el tablero para determinar la ventaja
    de la IA o el jugador en función de la cantidad de piezas alineadas.

    Param:
    - window: Una lista o sublista de cuatro elementos, que representa una "ventana" del tablero (puede ser una fila, columna o diagonal).
    - piece: La ficha del jugador que estamos evaluando (IA o jugador).

    Return:
    - score: Un valor numérico que representa la puntuación de la ventana evaluada.
    
    Lógica de puntuación:
    - Si la ventana tiene 4 fichas del jugador actual, se asigna una puntuación alta (100 puntos).
    - Si la ventana tiene 3 fichas del jugador y 1 espacio vacío, se asigna una puntuación intermedia (5 puntos).
    - Si la ventana tiene 2 fichas del jugador y 2 espacios vacíos, se asigna una puntuación baja (2 puntos).
    - Si la ventana tiene 3 fichas del oponente y 1 espacio vacío, se penaliza con puntos negativos (-4 puntos).
    """
    score = 0  # Inicializa la puntuación
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE  # Establece la pieza del oponente

    # Puntuación para 4 fichas alineadas del jugador
    if window.count(piece) == 4:
        score += 100

    # Puntuación para 3 fichas del jugador y 1 espacio vacío
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5

    # Puntuación para 2 fichas del jugador y 2 espacios vacíos
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    # Penalización para 3 fichas del oponente y 1 espacio vacío
    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score  # Retorna la puntuación de la ventana evaluada

# Calcular la puntuación total del tablero para la IA (o el jugador)
def score_position(board, piece):
    """
    Calcula una puntuación para la posición del tablero en función de las posibles jugadas de la IA.
    Se evalúan las filas, columnas, y diagonales para darle una puntuación alta a las jugadas favorables.
    
    Param:
    - board: La matriz que representa el tablero de juego.
    - piece: La ficha del jugador para la cual se está calculando la puntuación (IA o jugador).
    
    Return:
    - score: La puntuación total de la posición actual en el tablero.
    """
    score = 0  # Inicializa la puntuación en 0

    # Puntuación de las posiciones centrales del tablero
    # Las posiciones centrales son las más relevantes para la IA
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]  # Obtiene la columna central
    center_count = center_array.count(piece)  # Cuenta cuántas piezas del jugador están en la columna central
    score += center_count * 3  # Da una puntuación de 3 puntos por cada pieza en la columna central

    # Puntuación de las filas horizontales
    for r in range(ROW_COUNT):  # Recorre cada fila del tablero
        row_array = [int(i) for i in list(board[r, :])]  # Convierte la fila en una lista
        for c in range(COLUMN_COUNT - 3):  # Recorre las columnas en la fila, dejando espacio para ventanas de 4
            window = row_array[c:c + WINDOW_LENGTH]  # Toma una ventana de 4 elementos
            score += evaluate_window(window, piece)  # Evalúa la ventana y suma la puntuación correspondiente

    # Puntuación de las columnas verticales
    for c in range(COLUMN_COUNT):  # Recorre cada columna
        col_array = [int(i) for i in list(board[:, c])]  # Convierte la columna en una lista
        for r in range(ROW_COUNT - 3):  # Recorre las filas de la columna, dejando espacio para ventanas de 4
            window = col_array[r:r + WINDOW_LENGTH]  # Toma una ventana de 4 elementos en la columna
            score += evaluate_window(window, piece)  # Evalúa la ventana y suma la puntuación

    # Puntuación de las diagonales con pendiente positiva (\)
    for r in range(ROW_COUNT - 3):  # Recorre las filas hasta la cuarta última
        for c in range(COLUMN_COUNT - 3):  # Recorre las columnas hasta la cuarta última
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]  # Toma una ventana diagonal
            score += evaluate_window(window, piece)  # Evalúa la ventana diagonal y suma la puntuación

    # Puntuación de las diagonales con pendiente negativa (/)
    for r in range(ROW_COUNT - 3):  # Recorre las filas hasta la cuarta última
        for c in range(COLUMN_COUNT - 3):  # Recorre las columnas hasta la cuarta última
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]  # Toma una ventana diagonal invertida
            score += evaluate_window(window, piece)  # Evalúa la ventana diagonal y suma la puntuación

    return score  # Retorna la puntuación total de la posición del tablero

# Verificar si un nodo es terminal (fin del juego)
def is_terminal_node(board):
    """
    Verifica si el juego ha terminado, ya sea porque un jugador ha ganado o no hay más movimientos válidos.
    
    Param:
    - board: La matriz que representa el tablero de juego.
    
    Return:
    - True si el juego ha terminado (si hay un ganador o el tablero está lleno).
    - False si el juego continúa.
    """
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

# Obtener todas las ubicaciones válidas para un movimiento
def get_valid_locations(board):
    """
    Obtiene todas las columnas en las que se puede colocar una ficha, es decir, aquellas donde
    aún hay espacio para jugar.

    Param:
    - board: La matriz que representa el tablero de juego.
    
    Return:
    - valid_locations: Una lista de columnas en las que se puede realizar un movimiento válido.
    """
    valid_locations = []  # Lista para almacenar las columnas válidas
    for col in range(COLUMN_COUNT):  # Recorre todas las columnas
        if is_valid_location(board, col):  # Verifica si la columna tiene espacio para jugar
            valid_locations.append(col)  # Agrega la columna a la lista de ubicaciones válidas
    return valid_locations  # Retorna las columnas válidas

# Elegir la mejor jugada para la IA sin poda alpha-beta (algoritmo minimax)
def minimax(board, depth, maximizingPlayer):
    """
    Implementa el algoritmo minimax para que la IA elija la mejor jugada posible.
    El algoritmo evalúa el tablero recursivamente, alternando entre maximizar (IA) y minimizar (jugador).
    
    Param:
    - board: La matriz que representa el tablero de juego.
    - depth: La profundidad de la búsqueda. Cuanto mayor es la profundidad, más jugadas posibles se evalúan.
    - maximizingPlayer: Booleano que indica si es el turno de la IA (True) o del jugador (False).
    
    Return:
    - column: La columna elegida por la IA o el jugador.
    - value: La puntuación de esa jugada según el algoritmo minimax.
    """
    # Obtiene las columnas donde se puede jugar y verifica si el juego terminó
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    
    # Si la profundidad es cero o el juego ha terminado, se evalúa el estado actual
    if depth == 0 or is_terminal:
        if is_terminal:  # Si el juego ha terminado
            if winning_move(board, AI_PIECE):  # Si la IA ha ganado
                return (None, 100000000000000)  # Puntuación muy alta
            elif winning_move(board, PLAYER_PIECE):  # Si el jugador ha ganado
                return (None, -10000000000000)  # Puntuación muy baja
            else:  # Si es un empate
                return (None, 0)  # Empate
        else:  # Si la profundidad es cero (no se ha alcanzado el final)
            return (None, score_position(board, AI_PIECE))  # Evalúa la puntuación del tablero
    
    # Maximizar la puntuación (turno de la IA)
    if maximizingPlayer:
        value = -math.inf  # Inicializa la puntuación con un valor muy bajo
        column = random.choice(valid_locations)  # Elige una columna aleatoria como predeterminada
        
        # Recorre las posibles columnas para hacer el movimiento
        for col in valid_locations:
            row = get_next_open_row(board, col)  # Encuentra la siguiente fila disponible
            b_copy = board.copy()  # Copia el tablero para simular la jugada
            drop_piece(b_copy, row, col, AI_PIECE)  # Realiza la jugada de la IA
            new_score = minimax(b_copy, depth - 1, False)[1]  # Llama recursivamente al minimax para el jugador
            
            # Si la puntuación obtenida es mejor, actualiza el valor
            if new_score > value:
                value = new_score
                column = col
        
        return column, value  # Retorna la mejor columna y su puntuación
    
    else:  # Minimizar la puntuación (turno del jugador)
        value = math.inf  # Inicializa la puntuación con un valor muy alto
        column = random.choice(valid_locations)  # Elige una columna aleatoria como predeterminada
        
        # Recorre las posibles columnas para hacer el movimiento
        for col in valid_locations:
            row = get_next_open_row(board, col)  # Encuentra la siguiente fila disponible
            b_copy = board.copy()  # Copia el tablero para simular la jugada
            drop_piece(b_copy, row, col, PLAYER_PIECE)  # Realiza la jugada del jugador
            new_score = minimax(b_copy, depth - 1, True)[1]  # Llama recursivamente al minimax para la IA
            
            # Si la puntuación obtenida es peor, actualiza el valor
            if new_score < value:
                value = new_score
                column = col
        
        return column, value  # Retorna la mejor columna y su puntuación

# Elegir la mejor jugada para la IA con poda alpha-beta (algoritmo minimax mejorado)
def minimax_alpha_beta(board, depth, alpha, beta, maximizingPlayer):
    """
    Implementa el algoritmo minimax con poda alpha-beta para elegir la mejor jugada posible.
    La poda alpha-beta mejora la eficiencia del algoritmo minimax al reducir el número de nodos
    que se exploran en el árbol de decisiones.

    Param:
    - board: La matriz que representa el tablero de juego.
    - depth: La profundidad de la búsqueda. Cuanto mayor es la profundidad, más jugadas posibles se evalúan.
    - alpha: El valor máximo que el jugador maximiza está dispuesto a aceptar. Inicialmente, es -∞.
    - beta: El valor mínimo que el jugador minimiza está dispuesto a aceptar. Inicialmente, es ∞.
    - maximizingPlayer: Booleano que indica si es el turno de la IA (True) o del jugador (False).

    Return:
    - column: La columna elegida por la IA o el jugador.
    - value: La puntuación de esa jugada según el algoritmo minimax.
    """
    # Obtiene las columnas donde se puede jugar y verifica si el juego terminó
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    
    # Si la profundidad es cero o el juego ha terminado, se evalúa el estado actual
    if depth == 0 or is_terminal:
        if is_terminal:  # Si el juego ha terminado
            if winning_move(board, AI_PIECE):  # Si la IA ha ganado
                return (None, 100000000000000)  # Puntuación muy alta
            elif winning_move(board, PLAYER_PIECE):  # Si el jugador ha ganado
                return (None, -10000000000000)  # Puntuación muy baja
            else:  # Si es un empate
                return (None, 0)  # Empate
        else:  # Si la profundidad es cero (no se ha alcanzado el final)
            return (None, score_position(board, AI_PIECE))  # Evalúa la puntuación del tablero
    
    # Maximizar la puntuación (turno de la IA)
    if maximizingPlayer:
        value = -math.inf  # Inicializa la puntuación con un valor muy bajo
        column = random.choice(valid_locations)  # Elige una columna aleatoria como predeterminada
        
        # Recorre las posibles columnas para hacer el movimiento
        for col in valid_locations:
            row = get_next_open_row(board, col)  # Encuentra la siguiente fila disponible
            b_copy = board.copy()  # Copia el tablero para simular la jugada
            drop_piece(b_copy, row, col, AI_PIECE)  # Realiza la jugada de la IA
            new_score = minimax_alpha_beta(b_copy, depth - 1, alpha, beta, False)[1]  # Llama recursivamente al minimax para el jugador
            
            # Si la puntuación obtenida es mejor, actualiza el valor
            if new_score > value:
                value = new_score
                column = col
            
            # Actualiza alpha, el mejor valor que el jugador maximizador está dispuesto a aceptar
            alpha = max(alpha, value)
            
            # Si alpha es mayor o igual a beta, poda la rama (ya no es necesario explorarla)
            if alpha >= beta:
                break
                
        return column, value  # Retorna la mejor columna y su puntuación
    
    else:  # Minimizar la puntuación (turno del jugador)
        value = math.inf  # Inicializa la puntuación con un valor muy alto
        column = random.choice(valid_locations)  # Elige una columna aleatoria como predeterminada
        
        # Recorre las posibles columnas para hacer el movimiento
        for col in valid_locations:
            row = get_next_open_row(board, col)  # Encuentra la siguiente fila disponible
            b_copy = board.copy()  # Copia el tablero para simular la jugada
            drop_piece(b_copy, row, col, PLAYER_PIECE)  # Realiza la jugada del jugador
            new_score = minimax_alpha_beta(b_copy, depth - 1, alpha, beta, True)[1]  # Llama recursivamente al minimax para la IA
            
            # Si la puntuación obtenida es peor, actualiza el valor
            if new_score < value:
                value = new_score
                beta = min(beta, value)
            
            # Si alpha es mayor o igual a beta, poda la rama (ya no es necesario explorarla)
            if alpha >= beta:
                break
                
        return column, value  # Retorna la mejor columna y su puntuación

# ------------------------------------------------------------------------------------------------
#
# TD Learning 
#
# ------------------------------------------------------------------------------------------------

# Parámetros 
alpha = 0.1  # Tasa de aprendizaje, controla cuánto influye el nuevo conocimiento en el valor Q
gamma = 0.9  # Factor de descuento, representa la importancia de las recompensas futuras
epsilon = 0.1  # Tasa de exploración, controla cuánta probabilidad hay de tomar una acción aleatoria (explorar)

# Inicializar la tabla Q - Almacenará los valores Q para cada estado-acción. Se inicializa vacía.
Q = {}

# Función para obtener el estado como una cadena
def get_state(board):
    """
    Convierte el tablero de juego en un formato de cadena para usarlo como una clave en la tabla Q.
    Esto facilita la representación de los estados en Q-learning.
    
    Param:
    - board: El tablero de juego representado como una matriz de tamaño (ROW_COUNT, COLUMN_COUNT).
    
    Return:
    - Un string que representa el estado del tablero. Este string será utilizado como una clave
      para almacenar y acceder a los valores en la tabla Q.
    """
    return str(board)

# Función para elegir una acción basada en la política ε-greedy
def choose_action(state, valid_locations):
    """
    Selecciona una acción para el agente basado en la política ε-greedy.
    - Con probabilidad ε, selecciona una acción aleatoria (exploración).
    - Con probabilidad 1 - ε, selecciona la acción con el valor Q más alto (explotación).
    
    Param:
    - state: El estado actual del juego (representado como una cadena).
    - valid_locations: Lista de las columnas válidas donde el agente puede colocar una ficha.

    Return:
    - La columna seleccionada para colocar una ficha.
    """
    # Si no hay ubicaciones válidas (esquina del juego o error), retorna None.
    if not valid_locations:
        return None  # Evita que el código intente elegir una acción inválida

    # Obtiene los valores Q asociados con cada acción válida en el estado actual.
    q_values = [Q.get((state, a), 0) for a in valid_locations]
    
    # Si la lista de valores Q está vacía (no hay valores Q guardados), selecciona una acción aleatoria.
    if not q_values:  # Si la lista está vacía, elegir una acción aleatoria
        return random.choice(valid_locations)

    # Encuentra el valor Q máximo y selecciona la acción correspondiente.
    max_q = max(q_values)
    return valid_locations[q_values.index(max_q)]  # Retorna la columna con el mayor valor Q

# Función para actualizar la tabla Q utilizando la ecuación de Q-learning
def update_q(state, action, reward, next_state, next_action):
    """
    Actualiza el valor Q para una acción en un estado utilizando la fórmula de Q-learning.
    
    Param:
    - state: El estado actual del juego.
    - action: La acción tomada en el estado actual.
    - reward: La recompensa obtenida después de tomar la acción.
    - next_state: El siguiente estado después de realizar la acción.
    - next_action: La siguiente acción tomada en el siguiente estado (o None si es el final del juego).
    """
    q_value = Q.get((state, action), 0) # Obtiene el valor Q actual para el par (estado, acción), si no existe, asigna 0
    next_q_value = Q.get((next_state, next_action), 0) if next_action is not None else 0 # Si existe una acción en el siguiente estado, obtiene su valor Q; de lo contrario, asigna 0 (si es un estado terminal)
    Q[(state, action)] = q_value + alpha * (reward + gamma * next_q_value - q_value) # Actualiza la tabla Q con el nuevo valor calculado usando la ecuación de Q-learning

# Función que ejecuta un paso de aprendizaje Temporal Difference (TD) para un jugador.
def td_learning(board, depth):
    """
    Realiza un paso de aprendizaje TD para el agente. La función simula un turno en el juego
    y actualiza la tabla Q usando el aprendizaje TD.

    Param:
    - board: El estado actual del tablero de juego.
    - depth: La profundidad del árbol de decisión para la exploración del estado (actualmente no usado en la función).
    """
    # Obtiene el estado actual del tablero como una cadena para usar en la tabla Q.
    state = get_state(board)
    
    # Obtiene las columnas válidas donde se puede hacer un movimiento.
    valid_locations = get_valid_locations(board)
    
    # Elige la acción (columna) a tomar basada en la política ε-greedy.
    action = choose_action(state, valid_locations)

    # Si no hay jugadas posibles (ninguna ubicación válida), termina la función.
    if action is None:
        return  # Evita continuar si no hay jugadas posibles

    # Calcula la fila donde se debe colocar la ficha en la columna elegida.
    row = get_next_open_row(board, action)
    
    # Realiza el movimiento en el tablero colocando la ficha del jugador.
    drop_piece(board, row, action, PLAYER_PIECE)

    # Determina la recompensa basada en si el jugador gana, termina el juego o sigue jugando.
    if winning_move(board, PLAYER_PIECE):
        reward = 1  # Recompensa positiva si el jugador gana
    elif is_terminal_node(board):
        reward = 0  # Recompensa neutra si el juego termina sin un ganador
    else:
        reward = -0.1  # Recompensa negativa si no ha ocurrido un evento significativo (penalización por continuar)

    # Obtiene el nuevo estado del tablero después de hacer el movimiento.
    next_state = get_state(board)
    
    # Elige la siguiente acción en el nuevo estado con la política ε-greedy.
    next_action = choose_action(next_state, get_valid_locations(board))
    
    # Actualiza la tabla Q utilizando la fórmula de aprendizaje TD.
    update_q(state, action, reward, next_state, next_action)

# Función que simula un juego entre dos agentes utilizando TD Learning
def td_learning_vs_td_learning(board, depth):
    """
    Esta función simula un juego entre dos agentes que usan TD Learning. El juego se juega de manera alternada
    entre el jugador (PLAYER_PIECE) y la IA (AI_PIECE), actualizando las tablas Q de ambos agentes durante
    el transcurso del juego.
    
    Param:
    - board: El tablero actual del juego (matriz 2D).
    - depth: La profundidad para la función de evaluación en los agentes.
    """

    # Obtener el estado actual del tablero
    state = get_state(board)
    # Obtener las ubicaciones válidas para el próximo movimiento
    valid_locations = get_valid_locations(board)
    # Elegir una acción (columna) usando TD Learning para el jugador (PLAYER_PIECE)
    action = choose_action(state, valid_locations)
    # Determinar la fila donde caerá la pieza
    row = get_next_open_row(board, action)
    # Dejar la pieza en la ubicación correspondiente
    drop_piece(board, row, action, PLAYER_PIECE)

    # Evaluar la recompensa según el estado del juego
    if winning_move(board, PLAYER_PIECE):
        reward = 1  # El jugador gana
    elif is_terminal_node(board):
        reward = 0  # Empate o final del juego
    else:
        reward = -0.1  # Penalización por cada movimiento que no termine en victoria ni empate

    # Obtener el siguiente estado después del movimiento
    next_state = get_state(board)
    # Elegir la siguiente acción usando TD Learning
    next_action = choose_action(next_state, get_valid_locations(board))
    # Actualizar la tabla Q del jugador
    update_q(state, action, reward, next_state, next_action)

    # Si el juego no ha terminado, pasar a la siguiente jugada (IA)
    if not is_terminal_node(board):
        # Obtener el nuevo estado después de la jugada de la IA
        state = get_state(board)
        # Obtener las ubicaciones válidas para el próximo movimiento de la IA
        valid_locations = get_valid_locations(board)
        # Elegir una acción (columna) usando TD Learning para la IA
        action = choose_action(state, valid_locations)
        # Determinar la fila donde caerá la pieza de la IA
        row = get_next_open_row(board, action)
        # Dejar la pieza de la IA en la ubicación correspondiente
        drop_piece(board, row, action, AI_PIECE)

        # Evaluar la recompensa de la IA
        if winning_move(board, AI_PIECE):
            reward = 1  # La IA gana
        elif is_terminal_node(board):
            reward = 0  # Empate o final del juego
        else:
            reward = -0.1  # Penalización por movimiento no ganador ni empate

        # Obtener el siguiente estado después del movimiento de la IA
        next_state = get_state(board)
        # Elegir la siguiente acción usando TD Learning para la IA
        next_action = choose_action(next_state, get_valid_locations(board))
        # Actualizar la tabla Q de la IA
        update_q(state, action, reward, next_state, next_action)

# Función que ejecuta un paso de TD y un paso Minimax para hacer su movimiento.
def td_learning_vs_minimax(board, depth):
    """
    Realiza un paso de aprendizaje TD para el jugador (usando Q-learning) y luego
    ejecuta un movimiento para la IA utilizando el algoritmo Minimax.

    Param:
    - board: El estado actual del tablero de juego.
    - depth: La profundidad del árbol de decisión para el algoritmo Minimax (también utilizado en la IA).
    """
    # Obtiene el estado actual del tablero como una cadena para usar en la tabla Q.
    state = get_state(board)
    
    # Obtiene las columnas válidas donde se puede hacer un movimiento.
    valid_locations = get_valid_locations(board)
    
    # Elige la acción (columna) a tomar basada en la política ε-greedy.
    action = choose_action(state, valid_locations)

    # Calcula la fila donde se debe colocar la ficha en la columna elegida.
    row = get_next_open_row(board, action)
    
    # Realiza el movimiento en el tablero colocando la ficha del jugador.
    drop_piece(board, row, action, PLAYER_PIECE)

    # Determina la recompensa basada en si el jugador gana, termina el juego o sigue jugando.
    if winning_move(board, PLAYER_PIECE):
        reward = 1  # Recompensa positiva si el jugador gana
    elif is_terminal_node(board):
        reward = 0  # Recompensa neutra si el juego termina sin un ganador
    else:
        reward = -0.1  # Recompensa negativa si no ha ocurrido un evento significativo (penalización por continuar)

    # Obtiene el nuevo estado del tablero después de hacer el movimiento.
    next_state = get_state(board)
    
    # Elige la siguiente acción en el nuevo estado con la política ε-greedy.
    next_action = choose_action(next_state, get_valid_locations(board))
    
    # Actualiza la tabla Q utilizando la fórmula de aprendizaje TD.
    update_q(state, action, reward, next_state, next_action)

    # Si no ha terminado el juego, la IA toma su turno con Minimax.
    if not is_terminal_node(board):
        # La IA elige la mejor jugada utilizando Minimax.
        col, minimax_score = minimax(board, depth, True)
        
        # Calcula la fila donde se debe colocar la ficha para la IA.
        row = get_next_open_row(board, col)
        
        # Realiza el movimiento de la IA en el tablero.
        drop_piece(board, row, col, AI_PIECE)

# Función que ejecuta un paso de TD y un paso de Minimax con poda alpha-beta para hacer su movimiento.
def td_learning_vs_minimax_alpha_beta(board, depth):
    """
    Realiza un paso de aprendizaje TD para el jugador (usando Q-learning) y luego
    ejecuta un movimiento para la IA utilizando el algoritmo Minimax con poda alpha-beta.

    Parámetros:
    - board: El estado actual del tablero de juego.
    - depth: La profundidad del árbol de decisión para el algoritmo Minimax (también utilizado en la IA).
    """
    # Obtiene el estado actual del tablero como una cadena para usar en la tabla Q.
    state = get_state(board)
    
    # Obtiene las columnas válidas donde se puede hacer un movimiento.
    valid_locations = get_valid_locations(board)
    
    # Elige la acción (columna) a tomar basada en la política ε-greedy.
    action = choose_action(state, valid_locations)

    # Calcula la fila donde se debe colocar la ficha en la columna elegida.
    row = get_next_open_row(board, action)
    
    # Realiza el movimiento en el tablero colocando la ficha del jugador.
    drop_piece(board, row, action, PLAYER_PIECE)

    # Determina la recompensa basada en si el jugador gana, termina el juego o sigue jugando.
    if winning_move(board, PLAYER_PIECE):
        reward = 1  # Recompensa positiva si el jugador gana
    elif is_terminal_node(board):
        reward = 0  # Recompensa neutra si el juego termina sin un ganador
    else:
        reward = -0.1  # Recompensa negativa si no ha ocurrido un evento significativo (penalización por continuar)

    # Obtiene el nuevo estado del tablero después de hacer el movimiento.
    next_state = get_state(board)
    
    # Elige la siguiente acción en el nuevo estado con la política ε-greedy.
    next_action = choose_action(next_state, get_valid_locations(board))
    
    # Actualiza la tabla Q utilizando la fórmula de aprendizaje TD.
    update_q(state, action, reward, next_state, next_action)

    # Si no ha terminado el juego, la IA toma su turno con Minimax con poda alpha-beta.
    if not is_terminal_node(board):
        # La IA elige la mejor jugada utilizando Minimax con poda alpha-beta.
        col, minimax_score = minimax_alpha_beta(board, depth, -math.inf, math.inf, True)
        
        # Calcula la fila donde se debe colocar la ficha para la IA.
        row = get_next_open_row(board, col)
        
        # Realiza el movimiento de la IA en el tablero.
        drop_piece(board, row, col, AI_PIECE)

# -----------------------------------------------------------------------------------------------------
#
# FLUJO GENERAL DEL JUEGO
#
# -----------------------------------------------------------------------------------------------------

# Función para dibujar el tablero del juego en Pygame
def draw_board(board):
    """
    Dibuja el tablero del juego en la pantalla utilizando Pygame.
    Representa las casillas vacías y ocupadas por las piezas del jugador y la IA.

    Param:
    - board: El tablero de juego representado como una matriz 2D.
    """
    # Dibujar el fondo de las casillas vacías
    for c in range(COLUMN_COUNT):  # Recorre las columnas
        for r in range(ROW_COUNT):  # Recorre las filas
            # Dibuja un rectángulo de color SKYBLUE para cada casilla vacía
            pygame.draw.rect(screen, SKYBLUE, (c*SQUARESIZE, r*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            # Dibuja un círculo blanco para indicar la casilla vacía
            pygame.draw.circle(screen, WHITE, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)

    # Dibujar las piezas de los jugadores
    for c in range(COLUMN_COUNT):  # Recorre las columnas
        for r in range(ROW_COUNT):  # Recorre las filas
            # Si la casilla contiene una pieza del jugador
            if board[r][c] == PLAYER_PIECE:
                # Dibuja un círculo rojo para representar la pieza del jugador
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE + SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
            # Si la casilla contiene una pieza de la IA
            elif board[r][c] == AI_PIECE:
                # Dibuja un círculo amarillo para representar la pieza de la IA
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE + SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)

    # Actualiza la pantalla para reflejar los cambios
    pygame.display.update()

# Inicializar el tablero y variables
board = create_board()
print_board(board)
game_over = False
turn = random.randint(PLAYER, AI)

# Configurar la pantalla
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)

# Función para manejar la selección del modo de juego
def select_mode(mode_selected):
    """
    Maneja la selección del modo de juego. Asigna el modo seleccionado a la variable global `mode`
    y cierra la ventana de selección.

    Param:
    - mode_selected: El modo de juego seleccionado (por ejemplo, 'Jugador vs Jugador', 'Jugador vs IA').
    """
    global mode  # Declara la variable global `mode` para que pueda ser modificada
    mode = mode_selected  # Asigna el modo seleccionado a la variable `mode`
    root.destroy()  # Cierra la ventana actual (generalmente utilizada en interfaces gráficas Tkinter)

# Inicializar el popup para seleccionar el modo de juego
root = tk.Tk()
root.title("Seleccionar Modo de Juego")
root.geometry("350x250")  # Cambia las dimensiones según tus preferencias

# Crear botones para seleccionar el modo de juego
button1 = tk.Button(root, text="Humano vs MM W Pruning", command=lambda: select_mode("1"))
button1.pack(pady=10)

button2 = tk.Button(root, text="MM WO PAB vs MM W PAB", command=lambda: select_mode("2"))
button2.pack(pady=10)

button3 = tk.Button(root, text="TD Learning vs TD Learning", command=lambda: select_mode("3"))
button3.pack(pady=10)

button4 = tk.Button(root, text="TD Learning vs MM W PAB", command=lambda: select_mode("4"))
button4.pack(pady=10)

button5 = tk.Button(root, text="TD Learning vs MM WO PAB", command=lambda: select_mode("5"))
button5.pack(pady=10)

# Ejecutar el popup
root.mainloop()

# Bucle principal del juego
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if mode == "1": # Humano vs MM W Pruning
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
                # Preguntar por la entrada del Jugador 1
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(posx // SQUARESIZE)

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        if winning_move(board, PLAYER_PIECE):
                            label = myfont.render("Gana Jugador 1", 1, BLACK)
                            screen.blit(label, (30,10))
                            game_over = True

                        turn = AI
                        print_board(board)
                        draw_board(board)

            # Turno de la IA
            if turn == AI and not game_over:
                col, minimax_score = minimax_alpha_beta(board, 5, -math.inf, math.inf, True)

                if is_valid_location(board, col):
                    pygame.time.wait(500)
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, AI_PIECE)

                    if winning_move(board, AI_PIECE):
                        label = myfont.render("Gana Jugador 2", 1, BLACK)
                        screen.blit(label, (30,10))
                        game_over = True

                    print_board(board)
                    draw_board(board)

                    turn = PLAYER

        elif mode == "2": # MM WO PAB vs MM W PAB
            # Turno de la IA sin poda alpha-beta
            if turn == PLAYER and not game_over:
                col, minimax_score = minimax(board, 5, True)

                if is_valid_location(board, col):
                    pygame.time.wait(500)
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("Gana IA MM-WOP", 1, WHITE)
                        screen.blit(label, (30,10))
                        game_over = True

                    print_board(board)
                    draw_board(board)

                    turn = AI

            # Turno de la IA con poda alpha-beta
            if turn == AI and not game_over:
                col, minimax_score = minimax_alpha_beta(board, 5, -math.inf, math.inf, True)

                if is_valid_location(board, col):
                    pygame.time.wait(500)
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, AI_PIECE)

                    if winning_move(board, AI_PIECE):
                        label = myfont.render("Gana IA MM-WP", 1, WHITE)
                        screen.blit(label, (30,10))
                        game_over = True

                    print_board(board)
                    draw_board(board)

                    turn = PLAYER
        
        elif mode == "3": # TD Learning vs TD Learning
            # Turno de la IA 1 con TDL
            if turn == PLAYER and not game_over:
                td_learning_vs_td_learning(board, 5)
                print_board(board)
                draw_board(board)

                if winning_move(board, PLAYER_PIECE):
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    label = myfont.render("Gana TDL 1", 1, WHITE)
                    screen.blit(label, (20, 10))
                    pygame.display.update()
                    game_over = True
                elif winning_move(board, AI_PIECE):
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    label = myfont.render("Gana TDL 2", 1, WHITE)
                    screen.blit(label, (30, 10))
                    pygame.display.update()
                    game_over = True
                elif is_terminal_node(board):
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    label = myfont.render("¡Empate!", 1, WHITE)
                    screen.blit(label, (30, 10))
                    pygame.display.update()
                    game_over = True

                turn = AI
            
            # Turno de la IA 2 con TDL
            elif turn == AI and not game_over:
                td_learning_vs_td_learning(board, 5)
                print_board(board)
                draw_board(board)

                if winning_move(board, AI_PIECE):
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    label = myfont.render("Gana TDL 2", 1, WHITE)
                    screen.blit(label, (30, 10))
                    pygame.display.update()
                    game_over = True
                elif winning_move(board, PLAYER_PIECE):
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    label = myfont.render("Gana TDL 1", 1, WHITE)
                    screen.blit(label, (20, 10))
                    pygame.display.update()
                    game_over = True
                elif is_terminal_node(board):
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    label = myfont.render("¡Empate!", 1, WHITE)
                    screen.blit(label, (30, 10))
                    pygame.display.update()
                    game_over = True

                turn = PLAYER
                    
        elif mode == "4": # TD Learning vs MM W PAB
            # Turno IA con TDL 
            if turn == PLAYER and not game_over:
                td_learning_vs_minimax_alpha_beta(board, 5)
                print_board(board)
                draw_board(board)

                if winning_move(board, PLAYER_PIECE):
                    label = myfont.render("Gana TDL", 1, WHITE)
                    screen.blit(label, (30,10))
                    pygame.display.update()
                    game_over = True
                elif winning_move(board, AI_PIECE):
                    label = myfont.render("Gana MM W PAB", 1, WHITE)
                    screen.blit(label, (30,10))
                    pygame.display.update()
                    game_over = True
                elif is_terminal_node(board):
                    label = myfont.render("¡Empate!", 1, WHITE)
                    screen.blit(label, (30,10))
                    pygame.display.update()
                    game_over = True

                turn = AI
            
            # Turno de IA con Minimax con Poda Alpha-Betha
            elif turn == AI and not game_over:
                td_learning_vs_minimax_alpha_beta(board, 5)
                print_board(board)
                draw_board(board)

                if winning_move(board, AI_PIECE):
                    label = myfont.render("Gana TDL", 1, WHITE)
                    screen.blit(label, (30,10))
                    pygame.display.update()
                    game_over = True
                elif winning_move(board, PLAYER_PIECE):
                    label = myfont.render("Gana MM W PAB", 1, WHITE)
                    screen.blit(label, (30,10))
                    pygame.display.update()
                    game_over = True
                elif is_terminal_node(board):
                    label = myfont.render("¡Empate!", 1, WHITE)
                    screen.blit(label, (30,10))
                    pygame.display.update()
                    game_over = True

                turn = PLAYER

        elif mode == "5": # TD Learning vs MM WO PAB
            # Turno de TDL
            if turn == PLAYER and not game_over:
                td_learning_vs_minimax(board, 5)
                print_board(board)
                draw_board(board)

                if winning_move(board, PLAYER_PIECE):
                    label = myfont.render("Gana TDL", 1, WHITE)
                    screen.blit(label, (30,10))
                    pygame.display.update()
                    game_over = True
                elif winning_move(board, AI_PIECE):
                    label = myfont.render("Gana MM WO PAB", 1, WHITE)
                    screen.blit(label, (30,10))
                    pygame.display.update()
                    game_over = True
                elif is_terminal_node(board):
                    label = myfont.render("¡Empate!", 1, WHITE)
                    screen.blit(label, (30,10))
                    pygame.display.update()
                    game_over = True

                turn = AI
            
            # Turno de Minimax con Poda Alpha-Betha
            elif turn == AI and not game_over:
                td_learning_vs_minimax(board, 5)
                print_board(board)
                draw_board(board)

                if winning_move(board, AI_PIECE):
                    label = myfont.render("Gana TDL", 1, WHITE)
                    screen.blit(label, (30,10))
                    pygame.display.update()
                    game_over = True
                elif winning_move(board, PLAYER_PIECE):
                    label = myfont.render("Gana MM WO PAB", 1, WHITE)
                    screen.blit(label, (30,10))
                    pygame.display.update()
                    game_over = True
                elif is_terminal_node(board):
                    label = myfont.render("¡Empate!", 1, WHITE)
                    screen.blit(label, (30,10))
                    pygame.display.update()
                    game_over = True

                turn = PLAYER

    if game_over:
        pygame.time.wait(3000)

'''
# -----------------------------------------------------------------------------------------------------
#
# GRÁFICA DE RESULTADOS DE JUEGOS
#
# -----------------------------------------------------------------------------------------------------

# Función que simula una serie de juegos entre dos agentes y cuenta los resultados de victorias y empates.
def play_games(agent1, agent2, num_games, depth):
    """
    Juega múltiples juegos entre dos agentes (agent1 y agent2), registra los resultados de victorias y empates,
    y devuelve un diccionario con los resultados.
    
    Param:
    - agent1: El primer agente (jugador 1).
    - agent2: El segundo agente (jugador 2).
    - num_games: El número de juegos a jugar entre los dos agentes.
    - depth: La profundidad de búsqueda utilizada por los algoritmos Minimax o Minimax con poda alpha-beta.
    
    Return:
    - results: Un diccionario con el conteo de victorias de cada agente y los empates.
    """
    
    # Diccionario para almacenar los resultados de las partidas
    results = {"Agent1 Wins": 0, "Agent2 Wins": 0, "Draws": 0}

    # Jugar la cantidad de juegos especificada
    for _ in range(num_games):
        board = create_board()  # Crea un tablero vacío al inicio de cada juego
        game_over = False  # Variable para controlar si el juego ha terminado
        turn = random.randint(PLAYER, AI)  # Elige aleatoriamente quién empieza (jugador o IA)

        # Bucle principal del juego, se ejecuta hasta que el juego termine
        while not game_over:
            if turn == PLAYER:
                # Agent1 hace su movimiento (por ejemplo, TD Learning o un agente de otro tipo)
                agent1(board, depth)  # Ejecuta el movimiento de agent1, sin esperar retorno

                # Verificar si el jugador ha ganado o si el juego ha terminado en empate
                if winning_move(board, PLAYER_PIECE):
                    results["Agent1 Wins"] += 1  # Incrementa la victoria de Agent1
                    game_over = True  # Finaliza el juego
                elif is_terminal_node(board):
                    results["Draws"] += 1  # Incrementa el empate si no hay ganador
                    game_over = True
                turn = AI  # Cambia el turno a la IA (jugador 2)
            else:
                # Si agent2 es un algoritmo Minimax o Minimax con poda alpha-beta
                if agent2 in [minimax, minimax_alpha_beta]:
                    if agent2 == minimax:
                        col, _ = agent2(board, depth, True)  # Minimax con maximización de la IA
                    elif agent2 == minimax_alpha_beta:
                        col, _ = agent2(board, depth, -math.inf, math.inf, True)  # Minimax con poda alpha-beta
                # Si agent2 usa TD Learning, no se espera retorno de la función
                elif agent2 == td_learning:
                    agent2(board, depth)  # Ejecuta TD Learning sin retorno
                    col = None  # Evita errores si se usa otro bloque de código más abajo
                else:
                    col, _ = agent2(board, depth)  # Otros casos de agente de IA (por ejemplo, Q-learning)

                # Si la columna seleccionada es válida, se coloca la ficha de la IA
                if col is not None and is_valid_location(board, col):
                    row = get_next_open_row(board, col)  # Encuentra la fila disponible
                    drop_piece(board, row, col, AI_PIECE)  # Coloca la ficha de la IA en el tablero

                # Verificar si la IA ha ganado o si el juego ha terminado en empate
                if winning_move(board, AI_PIECE):
                    results["Agent2 Wins"] += 1  # Incrementa la victoria de Agent2
                    game_over = True  # Finaliza el juego
                elif is_terminal_node(board):
                    results["Draws"] += 1  # Incrementa el empate si no hay ganador
                    game_over = True
                turn = PLAYER  # Cambia el turno al jugador (agent1)

    # Retorna los resultados de las victorias y empates al final de los juegos
    return results

# Ejecutar 50 veces las 3 posibles opciones bajo las mismas condiciones
games_td_vs_td = play_games(td_learning, td_learning, 50, 5)
print("Termina TDL vs TDL")
games_td_vs_minimax = play_games(td_learning_vs_minimax, minimax, 50, 5)
print("Termina TDL vs MM WOP")
games_td_vs_minimax_ab = play_games(td_learning_vs_minimax_alpha_beta, minimax_alpha_beta, 50, 5)
print("Termina TDL vs MM WP")

# Función para graficar los resultados de los juegos (victorias y empates)
def plot_results(results, title, labels):
    """
    Genera un gráfico de barras que muestra los resultados de los juegos (victorias y empates).
    
    Param:
    - results: Un diccionario que contiene los resultados (victorias y empates) de las partidas.
    - title: El título que se mostrará en el gráfico.
    - labels: Las etiquetas que corresponden a las categorías de resultados (Ej. ["Agente 1", "Agente 2", "Empates"]).
    """
    
    values = list(results.values())  # Obtiene los valores del diccionario 'results' (victorias y empates)

    plt.figure(figsize=(8, 6))  # Define el tamaño de la figura del gráfico
    plt.bar(labels, values, color=['red', 'yellow', 'gray'])  # Crea el gráfico de barras con las etiquetas y los valores
    plt.title(title)  # Añade el título al gráfico
    plt.ylabel("Número de Juegos")  # Añade una etiqueta al eje Y (número de juegos)
    plt.show()  # Muestra el gráfico generado

# Gráficas Personalizadas para las 3 posibles opciones
plot_results(games_td_vs_td, "TD Learning vs TD Learning", ["TDL 1", "TDL 2", "Empate"])
plot_results(games_td_vs_minimax, "TD Learning vs Minimax sin Poda Alpha-Beta", ["TDL", "Minimax WOP", "Empate"])
plot_results(games_td_vs_minimax_ab, "TD Learning vs Minimax con Poda Alpha-Beta", ["TDL", "Minimax WP", "Empate"])
'''