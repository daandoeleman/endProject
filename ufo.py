import pygame

class Ufo:

    def __init__(self,screen_size,screen):
        self.screen_size = screen_size
        self.screen = screen
        self.x = 10
        self.y = 10
        self.speed = 2
        self.ufo_width = 100
        self.ufo_height = 50
        self.picture_UFO = pygame.image.load('obj_ufo.gif')
        self.ufo_image = pygame.transform.scale(self.picture_UFO, (self.ufo_width, self.ufo_height))

    def draw(self):
        self.screen.blit(self.ufo_image, (self.x, self.y))

    def update(self, search, maze,canon):

        if search.drawing_path is False:
            if self.speed > 0:
                maze.set_source(maze.grid[int((self.x+self.ufo_width/2)/maze.cell_width)][int((self.y+self.ufo_height/2)/maze.cell_height)])
            else:
                maze.set_source(maze.grid[int((self.x) / maze.cell_width)][int((self.y + self.ufo_height / 2) / maze.cell_height)+1])

            maze.set_target(maze.grid[int((canon.cart_position+120)/maze.cell_width)][int((canon.cart_y+120)/maze.cell_height)])
            search.a_star_search()

        if self.x <= 0:
            self.speed *= -1

        if self.x + self.ufo_width > self.screen_size[0]:
            self.speed *= -1

        self.x += self.speed
