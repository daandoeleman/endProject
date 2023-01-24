# method to display the clouds in the game by using grid elements as obstacles which the enemy needs to avoid

from grid_element import GridElement
from random import *
import pygame

class Clouds:

    def __init__(self, screen, screen_size):

        # store the screen to display on and its size
        self.screen = screen
        self.screen_size = screen_size

        # load the image for the clouds and scale it
        self.cloud = pygame.image.load('cloud.png')
        self.cloud_image = pygame.transform.scale(self.cloud, (100,100))

        # two arrays to store the positions of the clouds in the game
        self.clouds_x = []
        self.clouds_y = []

        # the width and the height of a cell in our grid
        self.cell_width = 20
        self.cell_height = 20

        # create the standard grid itself
        self.grid_size = (int(screen_size[0]/self.cell_width), int((screen_size[1])/self.cell_height))
        self.grid = []
        for x in range(self.grid_size[0]):
            self.grid.append([])
            for y in range(self.grid_size[1]):
                self.grid[x].append(GridElement(x, y, (self.cell_width, self.cell_height)))
        self.start = self.grid[30][3]
        self.target = self.grid[30][31]
        self.reset_all()

    # display all the images of the clouds
    def display(self):
        for i in range(len(self.clouds_x)):
            self.screen.blit(self.cloud_image, (self.clouds_x[i],self.clouds_y[i]))

    # method to reset all cells in the grid
    def reset_all(self):
        for row in self.grid:
            for cell in row:
                cell.reset_neighbours()
        self.reset_state()
        return None

    # method to reset all states of the cells
    def reset_state(self):
        for row in self.grid:
            for cell in row:
                cell.reset_state()
        self.start.set_distance(0)
        self.start.set_score(0)
        self.start.color = (0, 255, 0)
        self.target.color = (240, 60, 20)
        return None

    # method to set the source in the grid (starting point for the search)
    def set_source(self, cell):
        if cell != self.target:
            self.start = cell
            self.reset_state()

    # method to set the target in the grid (end point for the search)
    def set_target(self, cell):
        if cell != self.start:
            self.target = cell
            self.reset_state()

    # method to print the current maze
    def print_maze(self):
        transposed = list(zip(*self.grid))
        for row in transposed:
            print(row)
        return None

    # method to draw the current maze
    def draw_maze(self):
        # print all the lines in the grid, besides the outersquare lines
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                if row > 0 and row < self.grid_size[0] and col > 0 and col < self.grid_size[1]:
                    self.grid[row][col].draw_grid_element(self.screen)
        return None

    # method to find all possible neighbours of a certain cell
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

    # method to delete a link between two cells in the grid
    def del_link(self, cell1, cell2):
        if cell2 in cell1.neighbours:
            cell1.neighbours.remove(cell2)
        if cell1 in cell2.neighbours:
            cell2.neighbours.remove(cell1)
        return None

    # method to create a link between two cells in the grid
    def add_link(self, cell1, cell2):
        if cell1.manhattan_distance(cell2) == 1:
            cell1.neighbours.append(cell2)
            cell2.neighbours.append(cell1)
        return None

    # method to generate a certain number of clouds in the game
    def generate_clouds(self, number_of_clouds):

        # reset the grid
        self.reset_all()

        # generate an empty grid
        self.generate_open_maze()

        # calculate the required distance between clouds to fill up the screen
        self.distance_between_clouds = self.grid_size[0] / number_of_clouds

        # create two strokes with clouds at random positions
        for i in range(int(number_of_clouds)):
            self.cloud_builder(int((i - 1) * self.distance_between_clouds), randint(6, 8))
        for i in range(int(number_of_clouds-1)):
            self.cloud_builder(int((i) * self.distance_between_clouds + self.distance_between_clouds / 2), randint(11, 13))

    # method to build the clouds itself in the grid
    def cloud_builder(self, x, y):

        # add the coordinates to the array
        self.clouds_x.append(x*20+20)
        self.clouds_y.append(y*20)

        # create the necessary links to get a cloud shape in the grid
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

    # method to generate an open/empty maze
    def generate_open_maze(self):
        self.reset_all()
        for col in self.grid:
            for cell in col:
                cell.neighbours = self.possible_neighbours(cell)