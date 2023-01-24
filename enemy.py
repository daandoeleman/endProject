# the class which displays the enemy and controls the search

import pygame
import random
from search import Search

class Enemy:

    def __init__(self, screen, clouds):

        # store the screen to display on
        self.screen = screen

        # create the search algorithm to find paths through the clouds
        self.search = Search(clouds)

        # load all the images
        self.enemy1 = pygame.image.load('enemy1.png')
        self.enemy2 = pygame.image.load('enemy2.png')
        self.enemy3 = pygame.image.load('enemy3.png')
        self.enemy4 = pygame.image.load('enemy4.png')

        # scale all the images
        self.enemy_1 = pygame.transform.scale(self.enemy1, (75, 90))
        self.enemy_2 = pygame.transform.scale(self.enemy2, (75, 90))
        self.enemy_3 = pygame.transform.scale(self.enemy3, (75, 90))
        self.enemy_4 = pygame.transform.scale(self.enemy4, (75, 90))

        # at first just pick enemy 4 as the image for the enemy, later this will be randomly picked
        self.enemy = self.enemy_4

        # define the initial position of the enemy
        self.x = -50
        self.y = -50

        # define the timer and drawing speed to control the speed of movement of the enemy
        self.timer = 0
        self.drawing_speed = 20

    # display the enemy
    def display(self):
        self.screen.blit(self.enemy, (self.x - 25, self.y - 40))

    # update the enemy
    def update(self, maze, canon, ufo_speed, ufo_x, ufo_y):

        # if the enemy is not moving (for example when it has finished it path) then draw a new path
        if self.search.enemy_move is False:
            self.find_path(maze, canon, ufo_speed, ufo_x, ufo_y)
        # otherwise move along the previously calculated path
        else:
            # dependent on the drawing speed, follow the path stored in the coordinates lists
            if self.timer % self.drawing_speed == 0:
                self.x = self.search.x_coordinates[0] * 20
                self.y = self.search.y_coordinates[0] * 20

                # if not at target yet then remove the just made step from the lists
                if len(self.search.x_coordinates) > 1:
                    self.search.x_coordinates.pop(0)
                    self.search.y_coordinates.pop(0)

                # otherwise (so when at the end of the path) stop moving and reset the timer
                else:
                    self.search.enemy_move = False
                    self.timer = 0

            # increase the timer
            self.timer += 1

    # method to find a path by using the search algorithm
    def find_path(self, maze, canon, ufo_speed, ufo_x, ufo_y):

        if ufo_speed > 0:  # align the spawn position of the enemy with the image of the ufo
            # set the spawn position of the enemy at the position of the ufo
            maze.set_source(maze.grid[int((ufo_x + 100 / 2) / maze.cell_width)][int((ufo_y + 50 / 2) / maze.cell_height)])
        else:
            # set the spawn position of the enemy at the position of the ufo
            maze.set_source(maze.grid[int((ufo_x) / maze.cell_width)][int((ufo_y + 50 / 2) / maze.cell_height) + 1])

        # set the target of the enemy at the position of the cart
        maze.set_target(maze.grid[int((canon.cart_x + 120) / maze.cell_width)][int((canon.cart_y + 120) / maze.cell_height)])

        # search a path from the enemy to the cart
        self.search.a_star_search()

        # give the enemy a random color
        enemy_number = random.randint(1, 4)
        if enemy_number == 1:
            self.enemy = self.enemy_1
        elif enemy_number == 2:
            self.enemy = self.enemy_2
        elif enemy_number == 3:
            self.enemy = self.enemy_3
        elif enemy_number == 4:
            self.enemy = self.enemy_4