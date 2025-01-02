# File: pacman_game_simple.py
import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
GRID_SIZE = 30
FPS = 10
BLACK, WHITE, YELLOW, RED, BLUE = (0, 0, 0), (255, 255, 255), (255, 255, 0), (255, 0, 0), (0, 0, 255)

# Maze layout
MAZE = [
    "####################",
    "#........#.........#",
    "#.####.#.#.#.####..#",
    "#.#    #.#.#    #..#",
    "#.# ####.#.#### #..#",
    "#..........o.......#",
    "#.# ###### ######..#",
    "#.# #..........#...#",
    "#.# #.######.#.#...#",
    "#.................##",
    "####################"
]

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pacman")

# Create a clock object
clock = pygame.time.Clock()

# Load sprites
PACMAN_IMG = pygame.image.load("pacman.jpg")
PACMAN_IMG = pygame.transform.scale(PACMAN_IMG, (GRID_SIZE, GRID_SIZE))

GHOST_IMG = pygame.image.load("ghost.jpg")
GHOST_IMG = pygame.transform.scale(GHOST_IMG, (GRID_SIZE, GRID_SIZE))

POWER_PELLET = pygame.image.load("kebab.jpg")
POWER_PELLET = pygame.transform.scale(POWER_PELLET, (GRID_SIZE // 2, GRID_SIZE // 2))

# Helper Functions
def draw_maze():
    for row_idx, row in enumerate(MAZE):
        for col_idx, cell in enumerate(row):
            x, y = col_idx * GRID_SIZE, row_idx * GRID_SIZE
            if cell == "#":
                pygame.draw.rect(screen, BLUE, (x, y, GRID_SIZE, GRID_SIZE))
            elif cell == ".":
                pygame.draw.circle(screen, WHITE, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 4)
            elif cell == "o":
                screen.blit(POWER_PELLET, (x + GRID_SIZE // 4, y + GRID_SIZE // 4))

def can_move(x, y):
    col, row = x // GRID_SIZE, y // GRID_SIZE
    if MAZE[row][col] == "#":
        return False
    return True

def check_pellet(x, y):
    col, row = x // GRID_SIZE, y // GRID_SIZE
    if MAZE[row][col] == ".":
        MAZE[row] = MAZE[row][:col] + " " + MAZE[row][col+1:]
    elif MAZE[row][col] == "o":
        MAZE[row] = MAZE[row][:col] + " " + MAZE[row][col+1:]
        return True
    return False

# Classes
class Pacman:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.dx, self.dy = 0, 0
        self.image = PACMAN_IMG

    def move(self):
        new_x, new_y = self.x + self.dx * GRID_SIZE, self.y + self.dy * GRID_SIZE
        if can_move(new_x, new_y):
            self.x, self.y = new_x, new_y
            return check_pellet(self.x, self.y)
        return False

    def draw(self):
        # Rotate Pacman image based on movement direction
        if self.dx == 1:  # Moving right
            rotated_image = pygame.transform.rotate(self.image, 0)
        elif self.dx == -1:  # Moving left
            rotated_image = pygame.transform.rotate(self.image, 180)
        elif self.dy == 1:  # Moving down
            rotated_image = pygame.transform.rotate(self.image, 270)
        elif self.dy == -1:  # Moving up
            rotated_image = pygame.transform.rotate(self.image, 90)
        else:
            rotated_image = self.image  # No rotation
        screen.blit(rotated_image, (self.x, self.y))

class Ghost:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.dx, self.dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def move(self):
        new_x, new_y = self.x + self.dx * GRID_SIZE, self.y + self.dy * GRID_SIZE
        if not can_move(new_x, new_y) or random.random() < 0.1:  # Randomly change direction
            self.dx, self.dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        else:
            self.x, self.y = new_x, new_y

    def draw(self):
        screen.blit(GHOST_IMG, (self.x, self.y))

# Game Initialization
pacman = Pacman(GRID_SIZE, GRID_SIZE)
ghosts = [Ghost(GRID_SIZE * 10, GRID_SIZE * 5), Ghost(GRID_SIZE * 8, GRID_SIZE * 8)]

# Game Loop
while True:
    screen.fill(BLACK)
    draw_maze()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pacman.dx, pacman.dy = 0, -1
            elif event.key == pygame.K_DOWN:
                pacman.dx, pacman.dy = 0, 1
            elif event.key == pygame.K_LEFT:
                pacman.dx, pacman.dy = -1, 0
            elif event.key == pygame.K_RIGHT:
                pacman.dx, pacman.dy = 1, 0

    # Update game state
    pacman.move()
    for ghost in ghosts:
        ghost.move()

    # Check for collisions with ghosts
    for ghost in ghosts:
        if pacman.x == ghost.x and pacman.y == ghost.y:
            print("Game Over!")
            pygame.quit()
            sys.exit()

    # Check for win condition
    if all("." not in row for row in MAZE):
        print("You Win!")
        pygame.quit()
        sys.exit()

    # Draw game entities
    pacman.draw()
    for ghost in ghosts:
        ghost.draw()

    pygame.display.flip()
    clock.tick(FPS)
