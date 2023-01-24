# the class which creates the end screen, which is displayed if the player has lost the game

import pygame

class End_screen:

    def __init__(self, screen, screen_size):

        # store the screen to display on and its size
        self.screen = screen
        self.screen_size = screen_size

        # import the image for the end screen and scale it to the screen size
        self.end_screen = pygame.image.load('end_screen.png')
        self.end_screen_image = pygame.transform.scale(self.end_screen, (self.screen_size[0], self.screen_size[1]))

    def display(self):
        # display the end screen image
        self.screen.blit(self.end_screen_image, (0,0))
