import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
BOARD_WIDTH, BOARD_HEIGHT = 10, 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Shapes and their colors
SHAPES = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1, 1],
     [0, 1]],       # J shape
    [[1, 1, 1],
     [1, 0]],       # L shape
    [[1, 1],
     [1, 1]],       # O shape
    [[1, 1, 0],
     [0, 1, 1]],    # S shape
    [[0, 1, 1],
     [1, 1]],       # Z shape
    [[1, 1, 1],
     [0, 1]]        # T shape
]
SHAPE_COLORS = [
    CYAN,           # I shape
    BLUE,           # J shape
    ORANGE,         # L shape
    YELLOW,         # O shape
    GREEN,          # S shape
    RED,            # Z shape
    PURPLE          # T shape
]

# Initialize game variables
board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
current_shape = random.choice(SHAPES)
current_color = random.choice(SHAPE_COLORS)
shape_x = BOARD_WIDTH // 2 - len(current_shape[0]) // 2
shape_y = 0
game_over = False

# Initialize Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Tetris")

# Function to draw the board
def draw_board():
    screen.fill(BLACK)
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            pygame.draw.rect(screen, GRAY, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
            if board[y][x] != 0:
                pygame.draw.rect(screen, SHAPE_COLORS[board[y][x] - 1],
                                 (x * GRID_SIZE + 1, y * GRID_SIZE + 1, GRID_SIZE - 2, GRID_SIZE - 2))
    draw_current_shape()
    pygame.display.flip()

# Function to draw the current falling shape
def draw_current_shape():
    for y, row in enumerate(current_shape):
        for x, col in enumerate(row):
            if col:
                pygame.draw.rect(screen, current_color,
                                 ((shape_x + x) * GRID_SIZE + 1, (shape_y + y) * GRID_SIZE + 1,
                                  GRID_SIZE - 2, GRID_SIZE - 2))

# Function to check if the current shape can move in the specified direction
def can_move(dx, dy):
    for y, row in enumerate(current_shape):
        for x, col in enumerate(row):
            if col:
                nx, ny = shape_x + x + dx, shape_y + y + dy
                if nx < 0 or nx >= BOARD_WIDTH or ny >= BOARD_HEIGHT or (ny >= 0 and board[ny][nx]):
                    return False
    return True

# Function to place the current shape onto the board
def place_shape():
    for y, row in enumerate(current_shape):
        for x, col in enumerate(row):
            if col:
                board[shape_y + y][shape_x + x] = SHAPE_COLORS.index(current_color) + 1

# Function to remove completed lines
def remove_lines():
    global board
    new_board = []
    for row in board:
        if 0 not in row:
            new_board.append([0] * BOARD_WIDTH)
        else:
            new_board.append(row)
    lines_removed = BOARD_HEIGHT - len(new_board)
    board = [[0] * BOARD_WIDTH] * lines_removed + new_board
    return lines_removed

# Main game loop
clock = pygame.time.Clock()
while not game_over:
    clock.tick(10)  # Adjust game speed here

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and can_move(-1, 0):
                shape_x -= 1
            elif event.key == pygame.K_RIGHT and can_move(1, 0):
                shape_x += 1
            elif event.key == pygame.K_DOWN and can_move(0, 1):
                shape_y += 1
            elif event.key == pygame.K_UP:
                rotated_shape = list(zip(*reversed(current_shape)))
                if shape_x + len(rotated_shape[0]) <= BOARD_WIDTH and shape_y + len(rotated_shape) <= BOARD_HEIGHT:
                    old_shape = current_shape
                    current_shape = rotated_shape
                    if not can_move(0, 0):
                        current_shape = old_shape

    if can_move(0, 1):
        shape_y += 1
    else:
        place_shape()
        lines_removed = remove_lines()
        if lines_removed > 0:
            # Add scoring or other effects here
            pass
        current_shape = random.choice(SHAPES)
        current_color = random.choice(SHAPE_COLORS)
        shape_x = BOARD_WIDTH // 2 - len(current_shape[0]) // 2
        shape_y = 0
        if not can_move(0, 0):
            game_over = True

    draw_board()

# End of game
pygame.quit()
