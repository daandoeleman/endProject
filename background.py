from pygame import *
import math

class Background:

    def __init__(self, screen, screen_size):
        self.screen = screen
        self.screen_size = screen_size

        self.x = 400
        self.y = 700

        self.rails = image.load('rails.png')
        self.brick = image.load('brick.png')

        self.brick_size = 50

        self.rails_picture = transform.scale(self.rails, (self.brick_size, self.brick_size))
        self.brick_picture = transform.scale(self.brick, (self.brick_size, self.brick_size))

        self.tiles = math.ceil(screen_size[0] / self.brick_size) + 1

    def display(self):
        draw.rect(self.screen, (66, 149, 245), Rect(0, 0, self.screen_size[0], self.screen_size[1]-130))

        for i in range(0, self.tiles):
            self.screen.blit(self.brick_picture, (i * self.brick_size, self.screen_size[1] - self.brick_size))
            self.screen.blit(self.rails_picture, (i * self.brick_size, self.screen_size[1] - 1.6*self.brick_size))
