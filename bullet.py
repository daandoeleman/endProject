# the class for the behaviour of the bullets which come out of the cannon

import math
import pygame

class Bullet:
    def __init__(self, x, y, angle, shoot_intensity, screen):

        # store the variables needed for the behaviour of the bullet
        self.screen = screen
        self.x = x
        self.y = y
        self.angle = 1.1 * angle + 125
        self.shoot_intensity = shoot_intensity

        # the gravity working on the bullet
        self.gravity_force = 0.97

        # for left and right movement calculate with basic math the velocity in x and y direction
        if self.angle>90:
            self.speed_x = -1
            self.speed_y = -math.tan(math.radians(self.angle))
        else:
            self.speed_y = math.tan(math.radians(self.angle))
            self.speed_x = 1

        self.slope = self.speed_y

        # make sure that at (almost) vertical position (infinite slope, so infinite y speed) the y speed is limited
        if self.speed_y > 5:
            self.speed_y = 3
            self.speed_x = 0

        # apply the intensity to the speed (longer button press is faster shooting)
        self.speed_x *= shoot_intensity/3
        self.speed_y *= shoot_intensity/3

        # load, scale and rotate the image of the bullet
        self.bullet = pygame.image.load('bullet.png')
        self.bullet_scaled = pygame.transform.scale(self.bullet, (60, 40))
        self.picture_bullet = self.rot_center(self.bullet_scaled, self.angle-90)

    def display(self):
        # display the bullet
        self.screen.blit(self.picture_bullet, (self.x + 96, self.y + 108))

    def update(self):
        # update the position of the bullet
        self.x += self.speed_x
        self.y -= self.speed_y

        # update the speed with the gravity force
        self.speed_y *= self.gravity_force

        # if the bullet has come to a stop, then the bullet will start moving/accelerating down
        if self.speed_y<0.5 and self.speed_y > 0:
            self.gravity_force = 1.03
            self.speed_y *= -1

        # calculate and apply the correct angle dependent on if its moving either right, left or up
        if self.speed_x>0:
            self.angle = math.degrees(math.atan(self.speed_y/self.speed_x))
            self.picture_bullet = pygame.transform.rotate(self.bullet_scaled, self.angle-90)
        elif self.speed_x<0:
            self.angle = 90+math.degrees(math.atan(self.speed_y/self.speed_x))
            self.picture_bullet = pygame.transform.rotate(self.bullet_scaled, self.angle)
        else:
            self.angle = 90

    # method to rotate an image around its center from: https://www.pygame.org/wiki/RotateCenter
    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image