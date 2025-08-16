import pygame
import random

# Game settings
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
COLUMNS, ROWS = WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE
FPS = 60

# Define shapes
SHAPES = [
    [[1, 1, 1, 1]],                # I
    [[1, 1], [1, 1]],              # O
    [[0, 1, 0], [1, 1, 1]],        # T
    [[1, 0, 0], [1, 1, 1]],        # J
    [[0, 0, 1], [1, 1, 1]],        # L
    [[1, 1, 0], [0, 1, 1]],        # S
    [[0, 1, 1], [1, 1, 0]],        # Z
]

COLORS = [
    (0, 255, 255),
    (255, 255, 0),
    (128, 0, 128),
    (0, 0, 255),
    (255, 165, 0),
    (0, 255, 0),
    (255, 0, 0),
]

def rotate(shape):
    return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]

class Tetromino:
    def __init__(self):
        self.type = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.type]
        self.color = COLORS[self.type]
        self.x = COLUMNS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = rotate(self.shape)

def check_collision(board, tetromino, dx=0, dy=0, rotated_shape=None):
    shape = rotated_shape if rotated_shape else tetromino.shape
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                nx, ny = tetromino.x + x + dx, tetromino.y + y + dy
                if nx < 0 or nx >= COLUMNS or ny >= ROWS or (ny >= 0 and board[ny][nx]):
                    return True
    return False

def merge(board, tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                board[tetromino.y + y][tetromino.x + x] = tetromino.color

def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = ROWS - len(new_board)
    while len(new_board) < ROWS:
        new_board.insert(0, [0] * COLUMNS)
    return new_board, lines_cleared

def draw_board(screen, board, tetromino):
    for y in range(ROWS):
        for x in range(COLUMNS):
            color = board[y][x]
            if color:
                pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, tetromino.color, ((tetromino.x + x) * BLOCK_SIZE, (tetromino.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    board = [[0] * COLUMNS for _ in range(ROWS)]
    tetromino = Tetromino()
    fall_time = 0
    fall_speed = 0.5
    running = True
    score = 0

    while running:
        screen.fill((0, 0, 0))
        fall_time += clock.get_rawtime()
        clock.tick(FPS)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(board, tetromino, dx=-1):
                        tetromino.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if not check_collision(board, tetromino, dx=1):
                        tetromino.x += 1
                elif event.key == pygame.K_DOWN:
                    if not check_collision(board, tetromino, dy=1):
                        tetromino.y += 1
                elif event.key == pygame.K_UP:
                    new_shape = rotate(tetromino.shape)
                    if not check_collision(board, tetromino, rotated_shape=new_shape):
                        tetromino.shape = new_shape

        # Falling logic
        if fall_time / 1000 > fall_speed:
            if not check_collision(board, tetromino, dy=1):
                tetromino.y += 1
            else:
                merge(board, tetromino)
                board, lines = clear_lines(board)
                score += lines * 100
                tetromino = Tetromino()
                if check_collision(board, tetromino):
                    running = False  # Game over
            fall_time = 0

        draw_board(screen, board, tetromino)
        pygame.display.flip()

    print("Game Over! Your score:", score)
    pygame.quit()

if __name__ == "__main__":
    main()
