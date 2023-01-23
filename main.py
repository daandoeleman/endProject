import pygame
import sys
from keyboard_handler import KeyboardHandler
from clouds import Clouds
from search import Search
from background import Background
from ufo import Ufo
from canon import Canon
from end_screen import End_screen
from start_screen import Start_screen

class Game:
    """
    Initialize PyGame and create a graphical surface to write. Similar
    to void setup() in Processing
    """
    def __init__(self):
        pygame.init()

        self.screen_size = (1300, 800)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.keyboard_handler = KeyboardHandler()
        self.maze = Clouds(self.screen, self.screen_size)
        self.maze.generate_clouds(9)
        self.search = Search(self.maze, self.screen)
        self.ufo = Ufo(self.screen_size,self.screen)
        self.canon = Canon(self.screen, self.screen_size)
        self.background = Background(self.screen, self.screen_size)
        self.end_screen = End_screen(self.screen, self.screen_size)
        self.start_screen = Start_screen(self.screen, self.screen_size)
        self.game_finished = False
        self.game_started = False

    """
    Method 'game_loop' will be executed every frame to drive
    the display and handling of events in the background. 
    In Processing this is done behind the screen. Don't 
    change this, unless you know what you are doing.
    """
    def game_loop(self):
        self.handle_events()
        self.draw_components()
        self.update_game()

    def update_game(self):
        self.ufo.update(self.search, self.maze, self.canon)
        self.canon.read_data()
        self.canon.proces_data()
        self.canon.update()

        #  if there is a collision between the cart and the enemy
        if self.search.x > self.canon.cart_x+60 and self.search.x < self.canon.cart_x+160 and self.search.y > self.canon.cart_y+50 and self.search.y < self.canon.cart_y+150:
            # finish the game and show the end screen
            self.game_finished = True

            # reset the enemy so that the collision won't keep happening again and again and give it a new path to avoid keeping moving on the collision path
            self.maze.set_source(self.maze.grid[0][0])
            self.search.a_star_search()
            self.search.draw_path()

    def draw_components(self):

        if self.game_started is False:
            self.start_screen.display()
        elif self.game_finished is True:
            self.end_screen.display()
        else:
            self.screen.fill([92, 189, 85])
            self.background.display()
            self.maze.draw_maze()
            self.search.draw_path()
            self.ufo.draw()
            self.canon.display()

        pygame.display.flip()

    """
    Method 'handle_event' loop over all the event types and 
    handles them accordingly. 
    In Processing this is done behind the screen. Don't 
    change this, unless you know what you are doing.
    """
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.handle_key_down(event)
            if event.type == pygame.KEYUP:
                self.handle_key_up(event)
            if event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_pressed(event)
            if event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_released(event)

    """
    This method will store a currently pressed buttons 
    in list 'keyboard_handler.pressed'.
    """
    def handle_key_down(self, event):
        self.keyboard_handler.key_pressed(event.key)

        if event.key == pygame.K_SPACE:
            # start the game and stop showing the end screen
            self.game_started = True
            self.game_finished = False

            # set the enemy to the position of the ufo and start the search
            self.maze.set_source(self.maze.grid[int((self.ufo.x+self.ufo.ufo_width/2)/self.maze.cell_width)][int((self.ufo.y+self.ufo.ufo_height/2)/self.maze.cell_height)])
            self.search.a_star_search()
            self.search.draw_path()


    """
    This method will remove a released button 
    from list 'keyboard_handler.pressed'.
    """
    def handle_key_up(self, event):
        self.keyboard_handler.key_released(event.key)

    """
    Similar to void mouseMoved() in Processing
    """
    def handle_mouse_motion(self, event):
        pass

    """
    Similar to void mousePressed() in Processing
    """
    def handle_mouse_pressed(self, event):
        x = int(event.pos[0] / self.maze.cell_width)
        y = int(event.pos[1] / self.maze.cell_height)
        if event.button==1:
            self.maze.set_source(self.maze.grid[x][y])
            self.search.a_star_search()
        if event.button == 3:
            self.maze.set_target(self.maze.grid[x][y])

    """
    Similar to void mouseReleased() in Processing
    """
    def handle_mouse_released(self, event):
        pass

if __name__ == "__main__":
    game = Game()
    while True:
        game.game_loop()
