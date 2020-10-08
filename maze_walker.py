import pygame
import random
import time


WIDTH = 600
HEIGHT = 600
FPS = 60

# pygame window set up 
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Maze Generator')
clock = pygame.time.Clock()

# colours
BLACK = (0,   0,   0  )
WHITE = (192, 192, 192)
BLUE =  (0,   0,   128)
RED =   (255, 0,   0  )
GREEN = (0,   255, 0  )

# initial grid settings
cell_size = 60
grid_size = WIDTH // cell_size 

grid = []
stack = []
visited = []
openings = {}
path = {}
score = 0


# ------ grid builder
def build_grid(cell_size, grid_size):
    for i in range(grid_size):
        for j in range(grid_size):
            pygame.draw.rect(SCREEN, WHITE, (i * (cell_size), 
                                            j * (cell_size), 
                                            cell_size, cell_size), 1)
            grid.append((i * (cell_size), j * (cell_size)))

# ------ maze builder
def create_maze(x, y):
    # draw_nose(x, y)
    visited.append((x,y))
    stack.append((x,y))

    while stack:
        # check for neighbours
        neighbours = check_neighbourhood(x, y)

        if neighbours:
            cell_x, cell_y = random.choice(neighbours)
            # draw progression
            if cell_x == x and cell_y > y:
                grow_down(x,y)
                openings.setdefault((x,y),[]).append('down')
                openings.setdefault((cell_x,cell_y),[]).append('up')                
            elif cell_x == x and cell_y < y:
                grow_up(x,y)
                openings.setdefault((x,y),[]).append('up')
                openings.setdefault((cell_x,cell_y),[]).append('down')   
            elif cell_y == y and cell_x > x:
                grow_right(x,y)
                openings.setdefault((x,y),[]).append('right')
                openings.setdefault((cell_x,cell_y),[]).append('left')   
            else:
                grow_left(x,y) 
                openings.setdefault((x,y),[]).append('left')
                openings.setdefault((cell_x,cell_y),[]).append('right')   

            path[(cell_x, cell_y)] = (x, y)

            create_maze(cell_x, cell_y)

        else:
            # traceback
            x, y = stack.pop()
            draw_backtrack(x, y)
            cover_your_tracks(x, y)

# ------ set up maze creation functions
def check_neighbourhood(x,y):
    neighbours = []
    if (x + cell_size, y) in grid and (x + cell_size, y) not in visited:
        neighbours.append((x + cell_size, y))
    if (x - cell_size, y) in grid and (x - cell_size, y) not in visited:
        neighbours.append((x - cell_size, y))
    if (x, y + cell_size) in grid and (x, y + cell_size) not in visited:
        neighbours.append((x, y + cell_size))
    if (x, y - cell_size) in grid and (x, y - cell_size) not in visited:
        neighbours.append((x, y - cell_size))

    return neighbours

# ------ draw maze creator indicators:
def draw_nose(x, y):
    pygame.draw.rect(SCREEN, RED, (x + 1, y + 1, cell_size - 2, cell_size - 2))
    pygame.display.update()

def draw_backtrack(x, y):
    pygame.draw.rect(SCREEN, GREEN, (x + 1, y + 1, cell_size - 2, cell_size - 2))
    pygame.display.update()

def cover_your_tracks(x, y):
    pygame.draw.rect(SCREEN, BLUE, (x + 1, y + 1, cell_size - 2, cell_size - 2))
    pygame.display.update()


# ------ draw maze creation movemenet:
def grow_right(x, y):
    pygame.draw.rect(SCREEN, BLUE, (x + 1, y + 1,  2 * cell_size - 2, cell_size - 2))
    pygame.display.update()

def grow_down(x, y):
    pygame.draw.rect(SCREEN, BLUE, (x + 1, y + 1, cell_size - 2, 2 * cell_size - 2))
    pygame.display.update()

def grow_left(x, y):
    pygame.draw.rect(SCREEN, BLUE, (x - cell_size + 1, y + 1,  2 * cell_size - 2, cell_size - 2))
    pygame.display.update()

def grow_up(x, y):
    pygame.draw.rect(SCREEN, BLUE, (x + 1, y - cell_size + 1, cell_size - 2, 2 * cell_size - 2))
    pygame.display.update()


# ------ create a navigator class
class Navigator(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.location = (0,0)
        self.rect = self.image.get_rect()
        
    # navigator movement function
    def step(self, direction):
        compass = {'left': x - cell_size, 'right': x + cell_size, 'up': y - cell_size, 'down': y + cell_size}
        cover_your_tracks(x, y)
        if direction in 'left right':
            theseus.rect.x = compass[direction] + theseus.rect.width // 2
            theseus.location = (compass[direction], y)
        if direction in 'up down':
            theseus.rect.y = compass[direction] + theseus.rect.width // 2
            theseus.location = (x, compass[direction])

class Dot(pygame.sprite.Sprite):

    def __init__(self, size):
        super().__init__()
        self.image = pygame.Surface([size, size])
        self.image.fill(RED)
        self.size = size
        self.location = (0,0) # first dot appears in top left corner
        self.rect = self.image.get_rect()
        pygame.draw.circle(SCREEN, GREEN, (cell_size // 2, cell_size // 2), size , 0)

    def move(self):
        while self.location == theseus.location:
            x, y = random.choice(grid)
            self.location = (x, y)
            centered = (x + cell_size // 2, y + cell_size // 2)
        pygame.draw.circle(SCREEN, RED, centered, self.size , 0)


# ----------------- Action centre

# ------ make a maze
build_grid(cell_size, grid_size)
create_maze(0,0)  # start the maze in the top left corner

# ------ make a navigator
theseus = Navigator(GREEN, cell_size // 2, cell_size // 2)
start_x, start_y = grid[len(grid)-1]   # start the navigator on the bottom right corner
theseus.location = (start_x, start_y)
theseus.rect.x, theseus.rect.y = start_x + theseus.rect.width // 2, start_y + theseus.rect.height // 2
sprites = pygame.sprite.Group()
sprites.add(theseus)

# ------ make the red dot
dot = Dot(cell_size // 8)

# ------ pygame loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            x , y = theseus.location
            if event.key == pygame.K_DOWN:
                if (x, y + cell_size) in grid and 'down' in openings[(x,y)]:
                    theseus.step('down')
            if event.key == pygame.K_UP:
                if (x, y - cell_size) in grid and 'up' in openings[(x,y)]:
                    theseus.step('up')
            if event.key == pygame.K_LEFT:
                if (x - cell_size, y) in grid and 'left' in openings[(x,y)]:
                    theseus.step('left')
            if event.key == pygame.K_RIGHT:
                if (x + cell_size, y) in grid and 'right' in openings[(x,y)]:
                    theseus.step('right')   
        if theseus.location == dot.location:
            score += 1
            dot.move()
            print(f'score: {score}')


    sprites.draw(SCREEN)
    pygame.display.update()
