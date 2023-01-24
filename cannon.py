# the class for displaying the cannon, cart and bullets. This class also handles the connection with arduino

import pyfirmata
import inspect
import pygame
from bullet import Bullet

class Cannon:

    def __init__(self, screen, screen_size):

        # fix an issue with pyfirmata not working with python 3.11
        if not hasattr(inspect, 'getargspec'):
            inspect.getargspec = inspect.getfullargspec

        # connect to the arduino via port COM18
        self.board = pyfirmata.Arduino('COM18')
        self.it = pyfirmata.util.Iterator(self.board)
        self.it.start()

        # store the screen and its size
        self.screen = screen
        self.screen_size = screen_size

        # load the song for the shooting
        self.shooting_sound = pygame.mixer.Sound("shoot.mp3")

        # load the images for the cannon and cart and scale the n
        self.cannon = pygame.image.load('tank2.png')
        self.visor = pygame.image.load('cannon2.png')
        self.picture_cannon = pygame.transform.scale(self.cannon, (250, 250))

        # define the pins and counters
            # for the buttons:
        self.shoot_intensity = 10
        self.shoot_button = self.board.get_pin('d:10:i')
        self.drive_left_button = self.board.get_pin('d:12:i')
        self.drive_right_button = self.board.get_pin('d:11:i')

            # the potmeter:
        self.analog_input = self.board.get_pin('a:0:i')

            # the LEDs:
        self.led1 = self.board.get_pin('d:2:o')
        self.led2 = self.board.get_pin('d:3:o')
        self.led3 = self.board.get_pin('d:4:o')
        self.led4 = self.board.get_pin('d:5:o')
        self.led5 = self.board.get_pin('d:6:o')

            # H-bridge motor pins:
        self.IN1 = self.board.get_pin('d:7:o')
        self.IN2 = self.board.get_pin('d:8:o')
        self.EN = self.board.get_pin('d:9:o')

        # the initial position of the cart is at the center of the screen and give it a y coordinate
        self.cart_x = self.screen_size[0] / 2 - 125
        self.cart_y = 580

        # the speed of the cart
        self.cart_speed = 5

        # the angle of the visor
        self.angle = 0

        # an array to store all the bullets
        self.bullets = []

    def read_data(self):
        # read the state of the three buttons
        self.shoot_button_state = self.shoot_button.read()
        self.drive_left_button_state = self.drive_left_button.read()
        self.drive_right_button_state = self.drive_right_button.read()

        # read the potmeter value in a range from 0 to 60 degrees
        self.angle = (float(0 if self.analog_input.read() is None else -(self.analog_input.read()-0.2444)*309)*(60/100))

    def proces_data(self):
        # change the direction of movement of the DC motor dependent on which button is pressed
        if self.drive_left_button_state is True:
            self.IN1.write(0)                   # configure the H-bridge for moving right
            self.IN2.write(1)
            self.EN.write(1)                    # start moving the physical cart
            self.cart_x -= self.cart_speed      # move the cart on the screen also to the right
        elif self.drive_right_button_state is True:
            self.IN1.write(1)                   # configure the H-bridge for moving left
            self.IN2.write(0)
            self.EN.write(1)                    # start moving the physical cart
            self.cart_x += self.cart_speed      # move the cart on the screen also to the left
        else:
            self.EN.write(0)                    # if no button is pressed then don't move at all

        # if the shoot button is pressed then count how long its pressed
        if self.shoot_button_state is True:
            self.shoot_intensity += 1    # increase the counter and turn on the leds when the counter increases
            if self.shoot_intensity > 20:
                self.led1.write(1)
                if self.shoot_intensity > 30:
                    self.led2.write(1)
                    if self.shoot_intensity > 40:
                        self.led3.write(1)
                        if self.shoot_intensity > 50:
                            self.led4.write(1)
                            if self.shoot_intensity > 60:
                                self.led5.write(1)
                                self.shoot_intensity -= 1        # limit the counter to max 60, otherwise speed will be to high
        else:
            if self.shoot_intensity > 10:         # if the button is released then shoot with the given strength
                self.shoot(self.shoot_intensity)
                pygame.mixer.Sound.play(self.shooting_sound)

            # turn all the leds off and reset counter
            self.led1.write(0)
            self.led2.write(0)
            self.led3.write(0)
            self.led4.write(0)
            self.led5.write(0)
            self.shoot_intensity = 10

    def display(self):
        # display all the bullets on the screen
        for bullet in self.bullets:
            bullet.display()

        # display the visor at the right angle
        self.picture_visor = pygame.transform.rotate(pygame.transform.scale(self.visor, (300, 375)), self.angle+30)
        self.screen.blit(self.picture_visor, (self.cart_x - int(self.picture_visor.get_width() / 2) + 250 / 2, self.cart_y - int(self.picture_visor.get_height() / 2) + 250 / 2 + 10))

        # display the cannon
        self.screen.blit(self.picture_cannon, (self.cart_x, self.cart_y))

    def update(self):

        # avoid that the cart moves out of the screen
        if self.cart_x<30:
            self.cart_x = 30
        if self.cart_x>self.screen_size[0]-280:
            self.cart_x = self.screen_size[0]-280

        # update all the bullets
        for bullet in self.bullets:

            # remove bullets which are out of the screen
            if bullet.y>self.screen_size[1]:
                self.bullets.remove(bullet)
            # otherwise update the bullets which are still on the screen
            else:
                bullet.update()

    # if a bullet is shot, then add it to the array
    def shoot(self, shoot_intensity):
        self.bullets.append(Bullet(self.cart_x,self.cart_y, self.angle,shoot_intensity, self.screen))
