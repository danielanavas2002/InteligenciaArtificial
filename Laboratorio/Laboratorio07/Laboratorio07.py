import numpy as np
import pygame
import sys
import math
import random
import tkinter as tk

# Inicializar Pygame
pygame.init()

# Definir constantes
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)

SKYBLUE = (135, 206, 235)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

# Crear el tablero del juego
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# Soltar una ficha en el tablero
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Verificar si una columna es válida para un movimiento
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

# Obtener la siguiente fila abierta en una columna
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Imprimir el tablero (para propósitos de depuración)
def print_board(board):
    print(np.flip(board, 0))

# Verificar la condición de victoria
def winning_move(board, piece):
    # Verificar ubicaciones horizontales para ganar
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Verificar ubicaciones verticales para ganar
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Verificar diagonales con pendiente positiva
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Verificar diagonales con pendiente negativa
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

# Evaluar una ventana de cuatro posiciones para la puntuación de la IA
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score

# Calcular la puntuación del tablero para la IA
def score_position(board, piece):
    score = 0

    # Puntuación de las posiciones centrales del tablero
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Puntuación de las filas horizontales
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Puntuación de las columnas verticales
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Puntuación de las diagonales con pendiente positiva
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Puntuación de las diagonales con pendiente negativa
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

# Verificar si un nodo es terminal (fin del juego)
def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

# Obtener todas las ubicaciones válidas para un movimiento
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

# Elegir la mejor jugada para la IA sin poda alpha-beta (minimax)
def minimax(board, depth, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else: # Juego empatado
                return (None, 0)
        else: # Profundidad es cero
            return (None, score_position(board, AI_PIECE))
    
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, False)[1]
            
            if new_score > value:
                value = new_score
                column = col
                
        return column, value
    
    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, True)[1]
            
            if new_score < value:
                value = new_score
                column = col
                
        return column, value

# Elegir la mejor jugada para la IA con poda alpha-beta (minimax)
def minimax_alpha_beta(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else: # Juego empatado
                return (None, 0)
        else: # Profundidad es cero
            return (None, score_position(board, AI_PIECE))
    
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax_alpha_beta(b_copy, depth-1, alpha, beta, False)[1]
            
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
                
        return column, value
    
    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax_alpha_beta(b_copy, depth-1, alpha, beta, True)[1]
            
            if new_score < value:
                value = new_score
                beta = min(beta, value)
            if alpha >= beta:
                break
                
        return column, value


# Parámetros de Q-learning
alpha = 0.1  # Tasa de aprendizaje
gamma = 0.9  # Factor de descuento
epsilon = 0.1  # Tasa de exploración

# Inicializar la tabla Q
Q = {}

# Función para obtener el estado como una cadena
def get_state(board):
    return str(board)

# Función para elegir una acción usando épsilon-greedy
def choose_action(state, valid_locations):
    if random.uniform(0, 1) < epsilon:
        return random.choice(valid_locations)
    else:
        q_values = [Q.get((state, a), 0) for a in valid_locations]
        max_q = max(q_values)
        return valid_locations[q_values.index(max_q)]

# Función para actualizar la tabla Q
def update_q(state, action, reward, next_state, next_action):
    q_value = Q.get((state, action), 0)
    next_q_value = Q.get((next_state, next_action), 0)
    Q[(state, action)] = q_value + alpha * (reward + gamma * next_q_value - q_value)

def td_learning_vs_minimax_alpha_beta(board, depth):
    state = get_state(board)
    valid_locations = get_valid_locations(board)
    action = choose_action(state, valid_locations)
    row = get_next_open_row(board, action)
    drop_piece(board, row, action, PLAYER_PIECE)

    if winning_move(board, PLAYER_PIECE):
        reward = 1
    elif is_terminal_node(board):
        reward = 0
    else:
        reward = -0.1

    next_state = get_state(board)
    next_action = choose_action(next_state, get_valid_locations(board))
    update_q(state, action, reward, next_state, next_action)

    if not is_terminal_node(board):
        col, minimax_score = minimax_alpha_beta(board, depth, -math.inf, math.inf, True)
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, AI_PIECE)


def td_learning_vs_minimax(board, depth):
    state = get_state(board)
    valid_locations = get_valid_locations(board)
    action = choose_action(state, valid_locations)
    row = get_next_open_row(board, action)
    drop_piece(board, row, action, PLAYER_PIECE)

    if winning_move(board, PLAYER_PIECE):
        reward = 1
    elif is_terminal_node(board):
        reward = 0
    else:
        reward = -0.1

    next_state = get_state(board)
    next_action = choose_action(next_state, get_valid_locations(board))
    update_q(state, action, reward, next_state, next_action)

    if not is_terminal_node(board):
        col, minimax_score = minimax(board, depth, True)
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, AI_PIECE)

# Dibujar el tablero del juego en la pantalla
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, SKYBLUE, (c*SQUARESIZE, r*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, WHITE, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE + SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE + SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
    pygame.display.update()

# Inicializar el tablero y otras variables
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
    global mode
    mode = mode_selected
    root.destroy()

# Inicializar el popup para seleccionar el modo de juego
root = tk.Tk()
root.title("Seleccionar Modo de Juego")
root.geometry("350x225")  # Cambia las dimensiones según tus preferencias

# Crear botones para seleccionar el modo de juego
button1 = tk.Button(root, text="Humano vs MM W Pruning", command=lambda: select_mode("1"))
button1.pack(pady=10)

button2 = tk.Button(root, text="MM WO PAB vs MM W PAB", command=lambda: select_mode("2"))
button2.pack(pady=10)

button3 = tk.Button(root, text="TD Learning vs MM W PAB", command=lambda: select_mode("3"))
button3.pack(pady=10)

button4 = tk.Button(root, text="TD Learning vs MM WO PAB", command=lambda: select_mode("4"))
button4.pack(pady=10)

# Ejecutar el popup
root.mainloop()

# Bucle principal del juego
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if mode == "1":
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

        elif mode == "2":
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
                    
        elif mode == "3":
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

        elif mode == "4":
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
