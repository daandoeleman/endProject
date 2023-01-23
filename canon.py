import pyfirmata
import inspect
import pygame
from bullet import Bullet

class Canon:

    def __init__(self, screen, screen_size):
        if not hasattr(inspect, 'getargspec'):
            inspect.getargspec = inspect.getfullargspec

        self.board = pyfirmata.Arduino('COM18')
        self.screen = screen

        self.it = pyfirmata.util.Iterator(self.board)
        self.it.start()

        # Define the pins and counters
        # For the buttons:
        self.shoot_intensity = 0
        self.shoot_button = self.board.get_pin('d:10:i')
        self.drive_left_button = self.board.get_pin('d:12:i')
        self.drive_right_button = self.board.get_pin('d:11:i')

        # The potmeter:
        self.analog_input = self.board.get_pin('a:0:i')

        # The LEDs:
        self.led1 = self.board.get_pin('d:2:o')
        self.led2 = self.board.get_pin('d:3:o')
        self.led3 = self.board.get_pin('d:4:o')
        self.led4 = self.board.get_pin('d:5:o')
        self.led5 = self.board.get_pin('d:6:o')

        # H-bridge motor pins:
        self.IN1 = self.board.get_pin('d:7:o')
        self.IN2 = self.board.get_pin('d:8:o')
        self.EN = self.board.get_pin('d:9:o')

        # The position of the cart is at the center of the screen:
        self.cart_x = screen_size[0] / 2 - 125
        self.cart_speed = 3
        self.cart_y = 580
        self.angle = 0

        self.canon = pygame.image.load('tank2.png')
        self.visor = pygame.image.load('cannon2.png')
        self.bullets = []

        self.picture_canon = pygame.transform.scale(self.canon, (250, 250))

    def read_data(self):
        # Read the state of the buttons
        self.shoot_button_state = self.shoot_button.read()
        self.drive_left_button_state = self.drive_left_button.read()
        self.drive_right_button_state = self.drive_right_button.read()

        # The potmeter value in a range from 0 to 100 degrees
        self.angle = (float(0 if self.analog_input.read() is None else -(self.analog_input.read()-0.2444)*309)*(60/100))

        # print(shoot_button_state)
        # print(drive_left_button_state)
        # print(drive_right_button_state)
        # print(self.angle)

    def proces_data(self):
        # Change the direction of rotation dependent on which button is pressed
        if self.drive_left_button_state is True:
            self.IN1.write(0)
            self.IN2.write(1)
            self.EN.write(1)
            self.cart_x -= self.cart_speed
            # print("left")
            # print(self.cart_position)
        elif self.drive_right_button_state is True:
            self.IN1.write(1)
            self.IN2.write(0)
            self.EN.write(1)
            self.cart_x += self.cart_speed
            # print("right")
            # print(self.cart_position)
        else:
            self.EN.write(0)

        if self.shoot_button_state is True:
            self.shoot_intensity += 1    # increase the counter and turn on the leds when the counter increases
            if self.shoot_intensity > 10:
                self.led1.write(1)
                if self.shoot_intensity > 20:
                    self.led2.write(1)
                    if self.shoot_intensity > 30:
                        self.led3.write(1)
                        if self.shoot_intensity > 40:
                            self.led4.write(1)
                            if self.shoot_intensity > 50:
                                self.led5.write(1)
                                self.shoot_intensity -= 1        # limit the counter to max 50
        else:
            if self.shoot_intensity > 0:         # if the button is released then shoot with the given strength
                self.shoot(self.shoot_intensity)
                print("shoot", self.shoot_intensity)

            # turn all the leds off and reset counter
            self.led1.write(0)
            self.led2.write(0)
            self.led3.write(0)
            self.led4.write(0)
            self.led5.write(0)
            self.shoot_intensity = 0

    def display(self):
        self.picture_visor = pygame.transform.rotate(pygame.transform.scale(self.visor, (300, 375)), self.angle+30)

        self.screen.blit(self.picture_visor, (self.cart_x - int(self.picture_visor.get_width() / 2) + 250 / 2, self.cart_y - int(self.picture_visor.get_height() / 2) + 250 / 2 + 10))

        self.screen.blit(self.picture_canon, (self.cart_x, self.cart_y))

        # display all the bullets
        for bullet in self.bullets:
            bullet.display()

    def update(self):
        # update all the bullets
        for bullet in self.bullets:
            bullet.update()

            # remove bullets which are out of the screen
            if bullet.y<-200:
                self.bullets.remove(bullet)

    def shoot(self, shoot_intensity):
        self.bullets.append(Bullet(self.cart_x,self.cart_y, self.angle,shoot_intensity, self.screen))
