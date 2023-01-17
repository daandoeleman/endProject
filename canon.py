import pyfirmata
import time
import inspect

class Canon:

    def __init__(self):
        if not hasattr(inspect, 'getargspec'):
            inspect.getargspec = inspect.getfullargspec

        self.board = pyfirmata.Arduino('COM18')

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

        # The position of the cart:
        self.cart_position = 0

    def read_data(self):
        # Read the state of the buttons
        self.shoot_button_state = self.shoot_button.read()
        self.drive_left_button_state = self.drive_left_button.read()
        self.drive_right_button_state = self.drive_right_button.read()

        # The potmeter value in a range from 0 to 100 degrees
        self.potentiometer_value = float(0 if self.analog_input.read() is None else self.analog_input.read()-0.2444)*309

        # print(shoot_button_state)
        # print(drive_left_button_state)
        # print(drive_right_button_state)
        # print(potentiometer_value)

    def proces_data(self):
        # Change the direction of rotation dependent on which button is pressed
        if self.drive_left_button_state is True:
            self.IN1.write(0)
            self.IN2.write(1)
            time.sleep(0.02)
            self.EN.write(1)
            time.sleep(0.1)
            self.cart_position -= 1
            # print("left")
            print(self.cart_position)
        elif self.drive_right_button_state is True:
            self.IN1.write(1)
            self.IN2.write(0)
            time.sleep(0.02)
            self.EN.write(1)
            time.sleep(0.1)
            self.cart_position += 1
            # print("right")
            print(self.cart_position)
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
                print("shoot", self.shoot_intensity)

            # turn all the leds off and reset counter
            self.led1.write(0)
            self.led2.write(0)
            self.led3.write(0)
            self.led4.write(0)
            self.led5.write(0)
            self.shoot_intensity = 0

        # Small delay
        time.sleep(0.02)
