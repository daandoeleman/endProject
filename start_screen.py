from pygame import *

class Start_screen:

    def __init__(self, screen, screen_size):
        self.screen = screen
        self.screen_size = screen_size

        self.start_screen_image = image.load('start_screen.png')
        self.start_screen = transform.scale(self.start_screen_image, (self.screen_size[0], self.screen_size[1]))

    def display(self):
        self.screen.blit(self.start_screen, (0,0))
