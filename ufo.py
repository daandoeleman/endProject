# the class with the behaviour of the ufo and its spawned enemies

import pygame
from enemy import Enemy

class Ufo:

    def __init__(self, screen_size, screen, clouds):

        # store the screen to display on and its size
        self.screen_size = screen_size
        self.screen = screen

        # create an enemy
        self.enemy = Enemy(self.screen, clouds)

        # the initial position of the ufo
        self.x = 10
        self.y = 10

        # the movement speed of the ufo
        self.speed = 2

        # the size of the ufo
        self.ufo_width = 100
        self.ufo_height = 50

        # load the image for the ufo and scale it to its defined size
        self.picture_UFO = pygame.image.load('obj_ufo.gif')
        self.ufo_image = pygame.transform.scale(self.picture_UFO, (self.ufo_width, self.ufo_height))

    def display(self):
        # display the enemy
        self.enemy.display()

        # display the ufo
        self.screen.blit(self.ufo_image, (self.x, self.y))

    def update(self, clouds, canon):

        # update the enemy with the current situation
        self.enemy.update(clouds, canon, self.speed, self.x, self.y)

        # if the ufo moves out of the screen, then reverse
        if self.x <= 0:
            self.speed *= -1
        if self.x + self.ufo_width > self.screen_size[0]:
            self.speed *= -1

        # apply the speed of the ufo to its position
        self.x += self.speed