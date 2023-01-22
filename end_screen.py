from pygame import *

class End_screen:

    def __init__(self, screen, screen_size):
        self.screen = screen
        self.screen_size = screen_size

        self.end_screen_image = image.load('end_screen.png')
        self.end_screen = transform.scale(self.end_screen_image, (self.screen_size[0], self.screen_size[1]))

    def display(self):
        self.screen.blit(self.end_screen, (0,0))
