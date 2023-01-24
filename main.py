# AI practice final project by Daan Doeleman and Jules Verhagen
#
# It's a small minigame cannon shooter. In our game, aliens attempt to conquer the earth,
# but you may stop them by employing then-current technology, such as a cannon mounted on a cart.
# Shoot the aliens to protect our earth and don’t get caught by them. The fate of the entire globe
# depends on you! Interact with the game by using the provided cart and rails. Have fun!

import pygame
import sys
from keyboard_handler import KeyboardHandler
from search import Search
from background import Background
from ufo import Ufo
from clouds import Clouds
from canon import Canon
from end_screen import End_screen
from start_screen import Start_screen

class Game:

    def __init__(self):
        pygame.init()

        self.screen_size = (1300, 800)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.keyboard_handler = KeyboardHandler()
        self.clouds = Clouds(self.screen, self.screen_size)
        self.clouds.generate_clouds(9)
        self.search = Search(self.clouds, self.screen)
        self.ufo = Ufo(self.screen_size,self.screen)
        self.canon = Canon(self.screen, self.screen_size)
        self.background = Background(self.screen, self.screen_size)
        self.end_screen = End_screen(self.screen, self.screen_size)
        self.start_screen = Start_screen(self.screen, self.screen_size)
        self.game_finished = False
        self.game_started = False

        # initialise the songs and play the start song, songs are from: www.zapsplat.com
        self.start_song = pygame.mixer.Sound("startSong.mp3")
        self.theme_song = pygame.mixer.Sound("themeSong.mp3")
        self.end_song = pygame.mixer.Sound("endSong.mp3")
        self.enemy_killed_sound_effect = pygame.mixer.Sound("enemyKilled.mp3")
        pygame.mixer.Sound.play(self.start_song)

    def game_loop(self):
        self.handle_events()
        self.draw_components()
        self.update_game()

    # update the variables in the game
    def update_game(self):
        # if you are not at the start or and screen then update the game field
        if self.game_started is True and self.game_finished is False:
            self.ufo.update(self.search, self.clouds, self.canon)
            self.canon.read_data()
            self.canon.proces_data()
            self.canon.update()

        #  if there is a collision between the cart and the enemy
        if self.search.x > self.canon.cart_x+60 and self.search.x < self.canon.cart_x+160 and self.search.y > self.canon.cart_y+50 and self.search.y < self.canon.cart_y+150:
            # finish the game and show the end screen
            self.game_finished = True

            # stop the theme song and play the end song
            pygame.mixer.Sound.stop(self.theme_song)
            pygame.mixer.Sound.play(self.end_song)

            # reset the enemy so that the collision won't keep happening again and again and give it a new path to avoid keeping moving on the collision path
            self.clouds.set_source(self.clouds.grid[0][0])
            self.search.a_star_search()
            self.search.draw_path()

            # reset the drawing speed (the difficulty)
            self.search.drawing_speed = 20

            # remove all the bullets from the field
            for bullet in self.canon.bullets:
                self.canon.bullets.remove(bullet)

        # if there is a collision between the enemy and one of the bullets then reset enemy
        for bullet in self.canon.bullets:
            if self.search.x > bullet.x + 90 and self.search.x < bullet.x + 130 and self.search.y > bullet.y + 100 and self.search.y < bullet.y + 140:
                # reset the enemy to the position of the ufo and start the search
                self.clouds.set_source(self.clouds.grid[int((self.ufo.x + self.ufo.ufo_width / 2) / self.clouds.cell_width)][int((self.ufo.y + self.ufo.ufo_height / 2) / self.clouds.cell_height)])
                self.search.a_star_search()
                self.search.draw_path()

                # remove the bullet which killed the enemy
                self.canon.bullets.remove(bullet)

                # increase the drawing speed of the enemy, so increase the difficulty, but maximise it at 1
                self.search.drawing_speed = int(self.search.drawing_speed/1.2)
                if self.search.drawing_speed == 0:
                    self.search.drawing_speed = 1

                # play the enemy killed sound effect
                pygame.mixer.Sound.play(self.enemy_killed_sound_effect)

    # draw/display all the things on the screen
    def draw_components(self):
        if self.game_started is False:
            self.start_screen.display()
        elif self.game_finished is True:
            self.end_screen.display()
        else:
            self.screen.fill([92, 189, 85])
            self.background.display()

            # the maze cloud shapes
            # self.clouds.draw_maze()

            # the images of the clouds
            self.clouds.display()
            self.search.draw_path()
            self.ufo.draw()
            self.canon.display()

        pygame.display.flip()

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

    # what happens if a key is pressed
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
            self.search.a_star_search()
            self.search.draw_path()


    # remove a released button from list 'keyboard_handler.pressed'
    def handle_key_up(self, event):
        self.keyboard_handler.key_released(event.key)

    # mouse pressed function
    def handle_mouse_pressed(self, event):
        x = int(event.pos[0] / self.clouds.cell_width)
        y = int(event.pos[1] / self.clouds.cell_height)
        if event.button==1:
            self.clouds.set_source(self.clouds.grid[x][y])
            self.search.a_star_search()
        if event.button == 3:
            self.clouds.set_target(self.clouds.grid[x][y])

# run the game
if __name__ == "__main__":
    game = Game()
    while True:
        game.game_loop()
