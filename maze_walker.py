import pygame
import random
import time

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
FPS = 60

# pygame window set up 
def set_up(title):
    pygame.init()
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + cell_size))
    pygame.display.set_caption(title)
    clock = pygame.time.Clock()
    return SCREEN, clock

# colours
BLACK = (0,   0,   0  )
GREY =  (192, 192, 192)
BLUE =  (0,   0,   128)
RED =   (255, 0,   0  )
GREEN = (0,   255, 0  )

# initial variables
cell_size = 60
grid_size = SCREEN_WIDTH // cell_size 
grid = []
stack = []
visited = []
openings = {}
score = 0


# ----------- Functions --------------- #

# ------ grid builder
def build_grid(cell_size, grid_size):
    for i in range(grid_size):
        for j in range(grid_size):
            pygame.draw.rect(SCREEN, GREY, (i * (cell_size), 
                                            j * (cell_size), 
                                            cell_size, cell_size), 1)
            grid.append((i * (cell_size), j * (cell_size)))

# ------ maze builder
def create_maze(x, y):
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

            create_maze(cell_x, cell_y)

        else:
            # traceback
            x, y = stack.pop()

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

# ------ draw maze creation movemenet:
def grow_right(x, y):
    pygame.draw.rect(SCREEN, BLUE, (x + 1, y + 1,  2 * cell_size - 2, cell_size - 2))

def grow_down(x, y):
    pygame.draw.rect(SCREEN, BLUE, (x + 1, y + 1, cell_size - 2, 2 * cell_size - 2))

def grow_left(x, y):
    pygame.draw.rect(SCREEN, BLUE, (x - cell_size + 1, y + 1,  2 * cell_size - 2, cell_size - 2))

def grow_up(x, y):
    pygame.draw.rect(SCREEN, BLUE, (x + 1, y - cell_size + 1, cell_size - 2, 2 * cell_size - 2))

# ----- score update
def score_update(score):
    fontObj = pygame.font.Font('freesansbold.ttf', cell_size - 2)
    scoreboard = fontObj.render(f'Score: {score}  ', True, GREY, BLACK )
    scoreboardRect = scoreboard.get_rect()
    scoreboardRect.bottomleft = (0,  SCREEN_HEIGHT + cell_size)
    SCREEN.blit(scoreboard, scoreboardRect) 


# ----- end of game animation
def game_over():
    for cell in random.sample(grid, len(grid)):
        filler = pygame.draw.circle(SCREEN, GREEN, (cell[0] + cell_size // 2, cell[1] + cell_size // 2), cell_size // 2 , 0)
        pygame.display.update(filler)
        time.sleep(0.01)


# ----------- Classes --------------- #

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
        self.cover_your_tracks(x, y)
        if direction in 'left right':
            theseus.rect.x = compass[direction] + theseus.rect.width // 2
            theseus.location = (compass[direction], y)
        if direction in 'up down':
            theseus.rect.y = compass[direction] + theseus.rect.width // 2
            theseus.location = (x, compass[direction])
    
    def cover_your_tracks(self, x, y):
        pygame.draw.rect(SCREEN, BLUE, (x + 1, y + 1, cell_size - 2, cell_size - 2))
        pygame.display.update()


# ------ create a dot class

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


# ----------------- Action centre ----------------- #

# ------ make a maze
SCREEN, clock = set_up('Maze Walker')
build_grid(cell_size, grid_size)
create_maze(0, 0)  

# ------ make a navigator
theseus = Navigator(GREEN, cell_size // 2, cell_size // 2)
theseus.location = grid[len(grid)-1]   # start the navigator on the bottom right corner
theseus.rect.x = theseus.location[0] + theseus.rect.width // 2
theseus.rect.y = theseus.location[1] + theseus.rect.height // 2
sprites = pygame.sprite.Group()
sprites.add(theseus)

# ------ make the red dot
dot = Dot(cell_size // 8)

# ------ pygame loop
while True:
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
            if event.key == pygame.K_q:
                game_over()
                pygame.quit()

        if theseus.location == dot.location:
            score += 1
            dot.move()
            score_update(score)


    sprites.draw(SCREEN)
    pygame.display.update()
