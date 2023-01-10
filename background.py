from pygame import *

class Background:

    def __init__(self, screen, screen_size):
        self.screen = screen
        self.screen_size = screen_size

        self.x = 400
        self.y = 700

    def display(self):
        draw.rect(self.screen, (66, 149, 245), Rect(0, 0, self.screen_size[0], self.screen_size[1]-130))