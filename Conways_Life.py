import pygame
import random
# Initialize the pygame module 
pygame.init()

# Colors for the grid
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
GREEN = (57, 255, 20)

# GUI Dimensions
WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20

# Grid dimensions
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

# Refresh rate
FPS = 6000

# Create pygame GUI and clock 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Draws the grid
def draw_grid(positions):

    for position in positions:
        col, row  = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, GREEN, (*top_left, TILE_SIZE, TILE_SIZE))

    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, BLACK, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))
    
    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT ))

# Generates random color cells on the grid
def gen(num):
    return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])

def adjust_grid(positions):

    all_neighbors = set()
    new_positons = set()

    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) in [2, 3]:
            new_positons.add(position)

    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) == 3:
               new_positons.add(position)
    
    return new_positons

def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:

        if x + dx < 0 or x + dx > GRID_WIDTH:
            continue

        for dy in [-1, 0, 1]:

            if y + dy < 0 or y + dy > GRID_HEIGHT:
                continue 

            if dx == 0 and dy == 0:
                continue

            neighbors.append((x + dx, y + dy))
            
    return neighbors

# Main game loop 
def main():
    running = True
    playing = False
    count = 0
    update_freq = 120

    position = set()

    # Updates the events within the window 
    while running:
        clock.tick(FPS)

        if playing:
            count += 1
        
        if count >= update_freq:
            count = 0
            position = adjust_grid(position)
        
        pygame.display.set_caption('Playing' if playing else "Paused")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Logic that allows cells to be added mnaullt
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                if pos in position:
                    position.remove(pos)

                else:
                    position.add(pos)

            # handles keypresses
            if event.type == pygame.KEYDOWN:
                # Puases the simulation of the cells
                if event.key == pygame.K_SPACE:
                    playing = not playing
            
                # Clears the grid
                if event.key == pygame.K_c:
                    position = set()
                    playing = False
                    count = 0

                # Generates random cells onto the screen 
                if event.key == pygame.K_g:
                    position = gen(random.randrange(5, 10 )* GRID_WIDTH)

        screen.fill(GREY)
        draw_grid(position)
        pygame.display.update()


    pygame.quit()


if __name__ == "__main__":
    main()
