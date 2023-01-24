# the class which creates the background for the game and displays it

import pygame
import math
import random

class Background:

    def __init__(self, screen, screen_size):

        # store the screen to display on and its size
        self.screen = screen
        self.screen_size = screen_size

        # define the number of elements which will be displayed in the background
        self.brick_size = 50
        self.number_of_trees = 40
        self.number_of_flowers = 60
        self.number_of_bushes = 30
        self.number_of_grass = 30

        # load all the images used for the background
        self.rails = pygame.image.load('rails.png')
        self.brick = pygame.image.load('brick.png')
        self.tree = pygame.image.load('tree.png')
        self.bush = pygame.image.load('bush.png')
        self.grass = pygame.image.load('grass.png')
        self.end_stop_left = pygame.image.load('endStopLeft.png')
        self.end_stop_right = pygame.image.load('endStopRight.png')
        self.background = pygame.image.load('background.png')
        self.sky = pygame.image.load('sky.png')    # image from: https://toppng.com/show_download/165652/ftestickers-background-sky-star-sky-star/large

        # scale all the images
        self.rails_picture = pygame.transform.scale(self.rails, (self.brick_size, self.brick_size))
        self.brick_picture = pygame.transform.scale(self.brick, (self.brick_size, self.brick_size))
        self.tree_picture = pygame.transform.scale(self.tree, (60, 60))
        self.grass_picture = pygame.transform.scale(self.grass, (40, 40))
        self.bush_picture = pygame.transform.scale(self.bush, (25, 25))
        self.sky_picture = pygame.transform.scale(self.sky, (self.screen_size[0], 250))
        self.background_picture = pygame.transform.scale(self.background, (self.screen_size[0], self.screen_size[1]))
        self.end_stop_left_image = pygame.transform.scale(self.end_stop_left, (70,70))
        self.end_stop_right_image = pygame.transform.scale(self.end_stop_right, (70,70))

        # arrays to store all the positions for the trees, grass, bushes and flowers
        self.tree_positions_x = []
        self.tree_positions_y = []
        self.bush_positions_x = []
        self.bush_positions_y = []
        self.grass_positions_x = []
        self.grass_positions_y = []
        self.flower_positions_x = []
        self.flower_positions_y = []

        # an array to store the different flower images
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

            # choose a random flower image (a white, red or pink flower)
            self.flower_number = random.randint(1,3)

            # load the right image
            if self.flower_number == 1:
                self.flower_picture = pygame.image.load('flower1.png')
            elif self.flower_number == 2:
                self.flower_picture = pygame.image.load('flower2.png')
            elif self.flower_number == 3:
                self.flower_picture = pygame.image.load('flower3.png')

            # scale the image of the flower
            self.flower_picture = pygame.transform.scale(self.flower_picture, (25, 25))

            # add the image to the array with flower pictures
            self.flower_images.append(self.flower_picture)

        # calculate the number of tiles which fit on the screen
        self.tiles = math.ceil(screen_size[0] / self.brick_size) + 1

    def display(self):
            # the grass and sky on the background
            self.screen.blit(self.background_picture, (0, 0))

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