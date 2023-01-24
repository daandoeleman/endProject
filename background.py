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
        self.bush = image.load('bush.png')
        self.grass = image.load('grass.png')
        self.end_stop_left = image.load('endStopLeft.png')
        self.end_stop_right = image.load('endStopRight.png')
        self.sky = image.load('sky.png')    # image from: https://toppng.com/show_download/165652/ftestickers-background-sky-star-sky-star/large

        self.brick_size = 50
        self.number_of_trees = 40
        self.number_of_flowers = 60
        self.number_of_bushes = 30
        self.number_of_grass = 30

        self.rails_picture = transform.scale(self.rails, (self.brick_size, self.brick_size))
        self.brick_picture = transform.scale(self.brick, (self.brick_size, self.brick_size))
        self.tree_picture = transform.scale(self.tree, (60, 60))
        self.grass_picture = transform.scale(self.grass, (40, 40))
        self.bush_picture = transform.scale(self.bush, (25, 25))
        self.sky_picture = transform.scale(self.sky, (self.screen_size[0], 250))
        self.end_stop_left_image = transform.scale(self.end_stop_left, (70,70))
        self.end_stop_right_image = transform.scale(self.end_stop_right, (70,70))

        # arrays to store all the positions for the trees, grass, bushes and flowers
        self.tree_positions_x = []
        self.tree_positions_y = []
        self.bush_positions_x = []
        self.bush_positions_y = []
        self.grass_positions_x = []
        self.grass_positions_y = []
        self.flower_positions_x = []
        self.flower_positions_y = []

        # an array for the different flower images
        self.flower_images = []

        # fill the arrays with a random position for every tree, grass, bush and flower
        for i in range(0,self.number_of_trees):
            self.tree_positions_x.append(self.screen_size[0]/self.number_of_trees*i+random.randint(0,100))
            self.tree_positions_y.append(640+random.randint(0, 100))
        for i in range(0,self.number_of_grass):
            self.grass_positions_x.append(self.screen_size[0]/self.number_of_grass*i+random.randint(0,100))
            self.grass_positions_y.append(660+random.randint(0, 100))
        for i in range(0,self.number_of_bushes):
            self.bush_positions_x.append(self.screen_size[0]/self.number_of_bushes*i+random.randint(0,100))
            self.bush_positions_y.append(660+random.randint(0, 80))
        for i in range(0,self.number_of_flowers):
            self.flower_positions_x.append(self.screen_size[0]/self.number_of_flowers*i+random.randint(0,100))
            self.flower_positions_y.append(660+random.randint(0, 80))

            self.flower_number = random.randint(1,3)

            if self.flower_number == 1:
                self.flower_picture = image.load('flower1.png')
            elif self.flower_number == 2:
                self.flower_picture = image.load('flower2.png')
            elif self.flower_number == 3:
                self.flower_picture = image.load('flower3.png')

            self.flower_picture = transform.scale(self.flower_picture, (25, 25))

            self.flower_images.append(self.flower_picture)

        self.tiles = math.ceil(screen_size[0] / self.brick_size) + 1

    def display(self):
            draw.rect(self.screen, (66, 149, 245), Rect(0, 0, self.screen_size[0], self.screen_size[1]-130))

            # display the stars/the sky
            self.screen.blit(self.sky_picture, (0,0))

            # display all the grass
            for i in range(0, self.number_of_grass):
                self.screen.blit(self.grass_picture, (self.grass_positions_x[i], self.grass_positions_y[i]))

            # display all the flowers
            for i in range(0, self.number_of_flowers):
                self.screen.blit(self.flower_images[i], (self.flower_positions_x[i], self.flower_positions_y[i]))

            # display all the bushes
            for i in range(0, self.number_of_bushes):
                self.screen.blit(self.bush_picture, (self.bush_positions_x[i], self.bush_positions_y[i]))

            # display all the trees
            for i in range(0,self.number_of_trees):
                self.screen.blit(self.tree_picture, (self.tree_positions_x[i], self.tree_positions_y[i]))

            # display the brick wall and the rails on top of it
            for i in range(0, self.tiles):
                self.screen.blit(self.brick_picture, (i * self.brick_size, self.screen_size[1] - self.brick_size))
                self.screen.blit(self.rails_picture,
                                 (i * self.brick_size, self.screen_size[1] - 1.6 * self.brick_size))

            # display the two end stops for the cart
            self.screen.blit(self.end_stop_left_image, (48,690))
            self.screen.blit(self.end_stop_right_image, (1180, 690))