# AI practice final project of Daan Doeleman and Jules Verhagen

# It's a small minigame cannon shooter. In our game, aliens attempt to conquer the earth,
# but you may stop them by employing then-current technology, such as a cannon mounted on a cart.
# Shoot the aliens to protect our earth and don’t get caught by them. The fate of the entire globe
# depends on you! Interact with the game by using the provided cart and rails. Have fun!

import pygame
import sys
from keyboard_handler import KeyboardHandler
from background import Background
from ufo import Ufo
from clouds import Clouds
from cannon import Cannon
from end_screen import End_screen
from start_screen import Start_screen

class Game:

    def __init__(self):
        pygame.init()

        # create the window for the game
        self.screen_size = (1300, 800)
        self.screen = pygame.display.set_mode(self.screen_size)

        # create all objects needed for the game
        self.keyboard_handler = KeyboardHandler()
        self.clouds = Clouds(self.screen, self.screen_size)
        self.ufo = Ufo(self.screen_size,self.screen, self.clouds)
        self.cannon = Cannon(self.screen, self.screen_size)
        self.background = Background(self.screen, self.screen_size)
        self.end_screen = End_screen(self.screen, self.screen_size)
        self.start_screen = Start_screen(self.screen, self.screen_size)

        # generate 9 clouds
        self.clouds.generate_clouds(9)

        # the game is not finished and hasn't started yet
        self.game_finished = False
        self.game_started = False

        # initialise the songs, songs are from: www.zapsplat.com
        self.start_song = pygame.mixer.Sound("startSong.mp3")
        self.theme_song = pygame.mixer.Sound("themeSong.mp3")
        self.end_song = pygame.mixer.Sound("endSong.mp3")
        self.enemy_killed_sound_effect = pygame.mixer.Sound("enemyKilled.mp3")

        # start the intro song
        pygame.mixer.Sound.play(self.start_song)

    # loop the game
    def game_loop(self):
        self.handle_events()
        self.display()
        self.update()

    # update the variables in the game
    def update(self):
        # if you are not at the start or and screen then update the game field
        if self.game_started is True and self.game_finished is False:
            self.ufo.update(self.clouds, self.cannon)
            self.cannon.read_data()
            self.cannon.proces_data()
            self.cannon.update()

        #  if there is a collision between the cart and the enemy
        if self.ufo.enemy.x > self.cannon.cart_x+60 and self.ufo.enemy.x < self.cannon.cart_x+160 and self.ufo.enemy.y > self.cannon.cart_y+50 and self.ufo.enemy.y < self.cannon.cart_y+150:
            # finish the game and show the end screen
            self.game_finished = True

            # stop the theme song and play the end song
            pygame.mixer.Sound.stop(self.theme_song)
            pygame.mixer.Sound.play(self.end_song)

            # reset the enemy so that the collision won't keep happening again and again and give it a new path to avoid keeping moving on the collision path
            self.clouds.set_source(self.clouds.grid[0][0])
            self.ufo.enemy.find_path(self.clouds, self.cannon, self.ufo.speed, self.ufo.x, self.ufo.y)
            self.ufo.enemy.update(self.clouds, self.cannon, self.ufo.speed, self.ufo.x, self.ufo.y)

            # reset the drawing speed (the difficulty)
            self.ufo.enemy.drawing_speed = 20

            # remove all the bullets from the field
            for bullet in self.cannon.bullets:
                self.cannon.bullets.remove(bullet)
                self.cannon.update()

        # if there is a collision between the enemy and one of the bullets then reset enemy
        for bullet in self.cannon.bullets:
            if self.ufo.enemy.x > bullet.x + 90 and self.ufo.enemy.x < bullet.x + 130 and self.ufo.enemy.y > bullet.y + 100 and self.ufo.enemy.y < bullet.y + 140:
                # reset the enemy to the position of the ufo and start the search
                self.clouds.set_source(self.clouds.grid[int((self.ufo.x + self.ufo.ufo_width / 2) / self.clouds.cell_width)][int((self.ufo.y + self.ufo.ufo_height / 2) / self.clouds.cell_height)])
                self.ufo.enemy.find_path(self.clouds, self.cannon, self.ufo.speed, self.ufo.x, self.ufo.y)
                self.ufo.enemy.update(self.clouds, self.cannon, self.ufo.speed, self.ufo.x, self.ufo.y)

                # remove the bullet which killed the enemy
                self.cannon.bullets.remove(bullet)

                # increase the drawing speed of the enemy, so increase the difficulty, but maximise it at 1
                self.ufo.enemy.drawing_speed = int(self.ufo.enemy.drawing_speed/1.2)
                if self.ufo.enemy.drawing_speed == 0:
                    self.ufo.enemy.drawing_speed = 1

                # play the enemy killed sound effect
                pygame.mixer.Sound.play(self.enemy_killed_sound_effect)


    # display all the things on the screen
    def display(self):
        # display either the start or end screen or the normal game dependent on which state we are in
        if self.game_started is False:
            self.start_screen.display()
        elif self.game_finished is True:
            self.end_screen.display()
        else:
            self.background.display()           # display the background
            # self.clouds.draw_maze()           # the maze cloud shapes in the grid
            self.clouds.display()               # the images of the clouds
            self.ufo.display()                  # display the ufo and its enemies on the screen
            self.cannon.display()                # display the cannon on the screen

        pygame.display.flip()

    # what happens if a key is pressed, in our case only space is used
    def handle_key_down(self, event):
        self.keyboard_handler.key_pressed(event.key)

        if event.key == pygame.K_SPACE:

            # if switched from start to normal game screen, then stop start song and play themesong
            if self.game_started is False and self.game_finished is False:
                pygame.mixer.Sound.stop(self.start_song)
                pygame.mixer.Sound.play(self.theme_song)

            # if switched from end to normal game screen, then stop end song and play themesong
            if self.game_started is True and self.game_finished is True:
                pygame.mixer.Sound.stop(self.end_song)
                pygame.mixer.Sound.play(self.theme_song)

            # start the game and stop showing the end screen
            self.game_started = True
            self.game_finished = False

            # set the enemy to the position of the ufo and start the search
            self.clouds.set_source(self.clouds.grid[int((self.ufo.x + self.ufo.ufo_width / 2) / self.clouds.cell_width)][int((self.ufo.y + self.ufo.ufo_height / 2) / self.clouds.cell_height)])
            self.ufo.enemy.find_path(self.clouds, self.cannon, self.ufo.speed, self.ufo.x, self.ufo.y)
            self.ufo.enemy.update(self.clouds, self.cannon, self.ufo.speed, self.ufo.x, self.ufo.y)

    # handle all the different possible input events
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.handle_key_down(event)
            if event.type == pygame.KEYUP:
                self.handle_key_up(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_pressed(event)

    # remove a released button from list 'keyboard_handler.pressed'
    def handle_key_up(self, event):
        self.keyboard_handler.key_released(event.key)

    # mouse pressed function
    def handle_mouse_pressed(self, event):
        x = int(event.pos[0] / self.clouds.cell_width)
        y = int(event.pos[1] / self.clouds.cell_height)
        if event.button==1:
            self.clouds.set_source(self.clouds.grid[x][y])
            self.ufo.enemy.search.a_star_search()
        if event.button == 3:
            self.clouds.set_target(self.clouds.grid[x][y])

# run the game
if __name__ == "__main__":
    game = Game()
    while True:
        game.game_loop()
