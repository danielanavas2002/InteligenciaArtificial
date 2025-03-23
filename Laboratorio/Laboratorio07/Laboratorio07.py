import numpy as np
import pygame
import sys
import math
import random

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

# Bucle principal del juego
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

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

    if game_over:
        pygame.time.wait(3000)