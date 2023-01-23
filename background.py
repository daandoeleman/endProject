from pygame import *
import math
import random

class Background:

    def __init__(self, screen, screen_size):
        self.screen = screen
        self.screen_size = screen_size

        self.x = 400
        self.y = 700

        self.rails = image.load('rails.png')
        self.brick = image.load('brick.png')
        self.tree = image.load('tree.png')
        self.sky = image.load('sky.png')    # image from: https://toppng.com/show_download/165652/ftestickers-background-sky-star-sky-star/large

        self.brick_size = 50
        self.number_of_trees = 60

        self.rails_picture = transform.scale(self.rails, (self.brick_size, self.brick_size))
        self.brick_picture = transform.scale(self.brick, (self.brick_size, self.brick_size))
        self.tree_picture = transform.scale(self.tree, (50, 50))
        self.sky_picture = transform.scale(self.sky, (self.screen_size[0], 250))

        # a array to store all the positions for the trees
        self.tree_positions_x = []
        self.tree_positions_y = []

        # fill the arrays with a random position for every tree
        for i in range(0,self.number_of_trees):
            self.tree_positions_x.append(self.screen_size[0]/self.number_of_trees*i+random.randint(0,100))
            self.tree_positions_y.append(640+random.randint(0, 100))

        self.tiles = math.ceil(screen_size[0] / self.brick_size) + 1

    def display(self):
            draw.rect(self.screen, (66, 149, 245), Rect(0, 0, self.screen_size[0], self.screen_size[1]-130))

            self.screen.blit(self.sky_picture, (0,0))

            # display all the trees
            for i in range(0,self.number_of_trees):
                self.screen.blit(self.tree_picture, (self.tree_positions_x[i], self.tree_positions_y[i]))

            # display the brick wall and the rails on top of it
            for i in range(0, self.tiles):
                self.screen.blit(self.brick_picture, (i * self.brick_size, self.screen_size[1] - self.brick_size))
                self.screen.blit(self.rails_picture,
                                 (i * self.brick_size, self.screen_size[1] - 1.6 * self.brick_size))
