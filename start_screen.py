# the class for the start screen, which will be showed at the startup of the game

from pygame import *

class Start_screen:

    def __init__(self, screen, screen_size):

        # store the screen and its size to display on
        self.screen = screen
        self.screen_size = screen_size

        # load the image for the start screen and scale to the screensize
        self.start_screen_image = image.load('start_screen.png')
        self.start_screen = transform.scale(self.start_screen_image, (self.screen_size[0], self.screen_size[1]))

    def display(self):
        # display the start screen image
        self.screen.blit(self.start_screen, (0,0))
