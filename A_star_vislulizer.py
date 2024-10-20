import pygame
import math
from queue import PriorityQueue as pq

WIDTH = 900
HEIGHT = 900

SCREEN = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption("A* Path Finder Visualization")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 125, 0)
GRAY = (128, 128, 128)
TURQUIOSE = (64, 224, 208)

class Block:
    def __init__(self, rows, cols, width, total_rows):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.total_rows = total_rows
        self.x = rows * width
        self.y = cols * width
        self.color = WHITE
        self.neghbors = []
    
    def get_pos(self):
        return self.rows, self.cols
    
    def is_open(self):
        return self.color == GREEN
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_obs(self):
        return self.color == BLACK
    
    def is_closed(self):
        return self.color == YELLOW
    
    def is_goal(self):
        return self.color == TURQUIOSE
    
    def reset(self):
        self.color = WHITE
    
    def make_start(self):
        self.color = ORANGE
    
    def make_open(self):
        self.color = GREEN
    
    def make_goal(self):
        self.color = TURQUIOSE

    def make_path(self):
        self.color = PURPLE

    def make_obs(self):
        self.color = BLACK

    def make_closed(self):
        self.color = YELLOW

    def draw(self, scr):
        pygame.draw.rect(scr, self.color, (self.x, self.y, self.width, self.width))

    def Update_neghbors(self, grid):
        self.neghbors = []
        if self.rows < self.total_rows - 1 and not grid[self.rows + 1][self.cols].is_obs():  # Down
            self.neghbors.append(grid[self.rows + 1][self.cols])

        if self.rows > 0 and not grid[self.rows - 1][self.cols].is_obs():  # Up
            self.neghbors.append(grid[self.rows - 1][self.cols])

        if self.cols < self.total_rows - 1 and not grid[self.rows][self.cols + 1].is_obs():  # Right
            self.neghbors.append(grid[self.rows][self.cols + 1])

        if self.cols > 0 and not grid[self.rows][self.cols - 1].is_obs():  # Left
            self.neghbors.append(grid[self.rows][self.cols - 1])

    def __lt__(self, other):
        return False
    
def Huristic(block1, block2):
    x1, y1 = block1
    x2, y2 = block2

    return abs(x2 - x1) + abs(y2 - y1)

def Draw_path(previous, present, draw):
    while present in previous:
        present = previous[present]
        present.make_path()
        draw()

def A_star_search(Draw, grid, start, goal):
    cont = 0
    table = pq()
    table.put((0, cont, start))
    previous = {}
    g_func = {block: float("inf") for row in grid for block in row}
    g_func[start] = 0
    f_func = {block: float("inf") for row in grid for block in row}
    f_func[start] = Huristic(start.get_pos(), goal.get_pos())
    table_hash = {start}

    while not table.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        present = table.get()[2]
        table_hash.remove(present)

        if present == goal:
            Draw_path(previous, goal, Draw)
            goal.make_goal()
            start.make_start()
            return True
        
        for neighbor in present.neghbors:
            temp_g = g_func[present] + 1

            if temp_g < g_func[neighbor]:
                previous[neighbor] = present
                g_func[neighbor] = temp_g
                f_func[neighbor] = temp_g + Huristic(neighbor.get_pos(), goal.get_pos())
                if neighbor not in table_hash:
                    cont += 1
                    table.put((f_func[neighbor], cont, neighbor))
                    table_hash.add(neighbor)
                    neighbor.make_open()

        Draw()

        if present != start:
            present.make_closed()

    return False


def make_grid(rows, width):
    grid = []
    space = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            block = Block(i, j, space, rows)
            grid[i].append(block)

    return grid

def Draw_grid(win, rows, width):
    space = width // rows
    for i in range(rows):
        pygame.draw.line(win, GRAY, (0, i*space), (width, i*space))
        for j in range(rows):
            pygame.draw.line(win, GRAY, (j*space, 0), (j*space, width))
   
def Draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    Draw_grid(win, rows, width)
    pygame.display.update()

def click_pos(pos, rows, width):
    space = width // rows
    y, x = pos

    row = y // space
    col = x // space

    return row, col

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    Start = None
    goal = None

    Run = True
    while Run:
        Draw(win, grid, ROWS, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Run = False
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = click_pos(pos, ROWS, width)
                block = grid[row][col]
                if not Start and block != goal:
                    Start = block
                    Start.make_start()
                elif not goal and block != Start:
                    goal = block
                    goal.make_goal()
                elif block != Start and block != goal:
                    block.make_obs()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = click_pos(pos, ROWS, width)
                block = grid[row][col]
                block.reset()
                if block == Start:
                    Start = None
                elif block == goal:
                    goal = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and Start and goal:
                    for rows in grid:
                        for block in rows:
                            block.Update_neghbors(grid)

                    A_star_search(lambda: Draw(win, grid, ROWS, width), grid, Start, goal)

                if event.key == pygame.K_c:
                    Start = None
                    goal = None
                    grid = make_grid(ROWS, width)

    pygame.quit()
                    
main(SCREEN,WIDTH)