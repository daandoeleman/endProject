import random
from grid_element import GridElement
from random import *
from pygame import *

class Maze:
    """
        Generates a grid based maze based on GridElements
        This class also contains search algorithms for
        depth first, breath first, greedy and A* star search to
        solve the generated mazes
        """

    def __init__(self, screen, screen_size):
        self.screen = screen
        self.screen_size = screen_size
        self.cell_width = 20
        self.cell_height = 20
        self.grid_size = (int(screen_size[0]/self.cell_width), int((screen_size[1]-130)/self.cell_height))
        self.grid = []
        for x in range(self.grid_size[0]):
            self.grid.append([])
            for y in range(self.grid_size[1]):
                self.grid[x].append(GridElement(x, y, (self.cell_width, self.cell_height)))
        self.start = self.grid[30][3]
        self.target = self.grid[30][31]
        self.reset_all()


    """
    Resets the GridElements of the maze
    """

    def reset_all(self):
        for row in self.grid:
            for cell in row:
                cell.reset_neighbours()
        self.reset_state()
        return None

    def reset_state(self):
        for row in self.grid:
            for cell in row:
                cell.reset_state()
        self.start.set_distance(0)
        self.start.set_score(0)
        self.start.color = (0, 255, 0)
        self.target.color = (240, 60, 20)
        return None

    def set_source(self, cell):
        if cell != self.target:
            self.start = cell
            self.reset_state()

    def set_target(self, cell):
        if cell != self.start:
            self.target = cell
            self.reset_state()

    def print_maze(self):
        transposed = list(zip(*self.grid))
        for row in transposed:
            print(row)
        return None

    def draw_maze(self, surface):
        # print all the lines in the grid, besides the outersquare lines
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                if row > 0 and row < self.grid_size[0]-1 and col > 0 and col < self.grid_size[1]-1:
                    self.grid[row][col].draw_grid_element(surface)
        return None

    def possible_neighbours(self, cell):
        neighbours = []
        if cell.position[0] > 0:  # North
            neighbours.append(self.grid[cell.position[0] - 1][cell.position[1]])
        if cell.position[0] < self.grid_size[0] - 1:  # East
            neighbours.append(self.grid[cell.position[0] + 1][cell.position[1]])
        if cell.position[1] < self.grid_size[1] - 1:  # South
            neighbours.append(self.grid[cell.position[0]][cell.position[1] + 1])
        if cell.position[1] > 0:  # West
            neighbours.append(self.grid[cell.position[0]][cell.position[1] - 1])
        return neighbours

    def del_link(self, cell1, cell2):
        if cell2 in cell1.neighbours:
            cell1.neighbours.remove(cell2)
        if cell1 in cell2.neighbours:
            cell2.neighbours.remove(cell1)
        return None

    def add_link(self, cell1, cell2):
        if cell1.manhattan_distance(cell2) == 1:
            cell1.neighbours.append(cell2)
            cell2.neighbours.append(cell1)
        return None

    """
     Generate the maze based on depth first search 
     """

    def generate_clouds(self, number_of_clouds):

        self.distance_between_clouds = self.grid_size[0]/number_of_clouds
        self.reset_all()
        self.generate_open_maze()

        for i in range(int(number_of_clouds)):
            self.large_cloud(int((i-1)*self.distance_between_clouds),randint(4, 6))

        for i in range(int(number_of_clouds-1)):
            self.large_cloud(int((i)*self.distance_between_clouds+self.distance_between_clouds/2),randint(9, 11))


    def large_cloud(self,x,y):
        self.del_link(self.grid[x+2][y], self.grid[x+2][y+1])
        self.del_link(self.grid[x+3][y], self.grid[x+3][y+1])
        self.del_link(self.grid[x+4][y], self.grid[x+4][y+1])
        self.del_link(self.grid[x+4][y+1], self.grid[x+5][y+1])
        self.del_link(self.grid[x+5][y+2], self.grid[x+5][y+1])
        self.del_link(self.grid[x+5][y+2], self.grid[x+6][y+2])
        self.del_link(self.grid[x+3][y+3], self.grid[x+3][y+4])
        self.del_link(self.grid[x+4][y+3], self.grid[x+4][y+4])
        self.del_link(self.grid[x+4][y+3], self.grid[x+5][y+3])
        self.del_link(self.grid[x+5][y+3], self.grid[x+5][y+2])
        self.del_link(self.grid[x+2][y+3], self.grid[x+2][y+4])
        self.del_link(self.grid[x+1][y+3], self.grid[x+2][y+3])
        self.del_link(self.grid[x+1][y+3], self.grid[x+1][y+2])
        self.del_link(self.grid[x+1][y+2], self.grid[x][y+2])
        self.del_link(self.grid[x+1][y+1], self.grid[x+1][y+2])
        self.del_link(self.grid[x+1][y+1], self.grid[x+2][y+1])

        return None

    def generate_open_maze(self):
        self.reset_all()
        for col in self.grid:
            for cell in col:
                cell.neighbours = self.possible_neighbours(cell)