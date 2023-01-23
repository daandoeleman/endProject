import math
import pygame

class Bullet:
    def __init__(self, x, y, angle, shoot_intensity, screen):

        self.screen = screen
        self.x = x
        self.y = y
        self.angle = 1.1 * angle + 125

        # for left and right calculate with basic math the velocity in x and y direction
        if self.angle>90:
            self.speed_x = -1
            self.speed_y = -math.tan(math.radians(self.angle))
        else:
            self.speed_y = math.tan(math.radians(self.angle))
            self.speed_x = 1

        # make sure that at (almost) vertical position (infinite slope, so infinite y speed) the y speed is limited
        if self.speed_y > 5:
            self.speed_y = 3
            self.speed_x = 0

        # apply the intensity to the speed (longer button press is faster shooting)
        self.speed_x *= shoot_intensity/3
        self.speed_y *= shoot_intensity/3

        self.bullet = pygame.image.load('bullet.png')
        self.bullet_scaled = pygame.transform.scale(self.bullet, (60, 40))
        self.picture_bullet = self.rot_center(self.bullet_scaled, self.angle-90)

    def display(self):
        self.screen.blit(self.picture_bullet, (self.x + 96, self.y + 108))

    def update(self):
        self.x += self.speed_x
        self.y -= self.speed_y

    # method to rotate an image around its center from: https://www.pygame.org/wiki/RotateCenter
    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image