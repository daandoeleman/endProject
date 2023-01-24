# method to draw a grit with its walls/elements. This code is used from the tutorials and only has small changes

from pygame import draw

class GridElement:

    def __init__(self, x, y, size):
        self.position = (x, y)
        self.neighbours = []
        self.size = (size[0], size[1])
        self.parent = None
        self.distance = None
        self.score = None
        self.color = (66, 149, 245)

    # overload the equals operator
    def __eq__(self, other):
        return self.position == other.position

    # overload the less than operator
    def __lt__(self, other):
        return (self.score is not None) and (other.score is None or self.score < other.score)

    # overload the hash operator
    def __hash__(self):
        return hash(self.position)

    # overload the string representation of the object
    def __repr__(self):
        return "[%s, %s]" % (self.position, self.score)

    # remove all neighbours
    def reset_neighbours(self):
        self.neighbours = []

    # sets the state of the GridElement
    def reset_state(self):
        self.parent = None
        self.score = None
        self.distance = None
        self.color = (66, 149, 245)

    # get all neighbouring nodes
    def get_neighbours(self):
        return self.neighbours[:]

    # method to calculate the manhattan distance from one node to another
    def manhattan_distance(self, other):
        x_distance = abs(self.position[0] - other.position[0])
        y_distance = abs(self.position[1] - other.position[1])
        return x_distance + y_distance

    # method to get the direction of a certain node
    def direction(self, other):
        return other.position[0] - self.position[0], other.position[1] - self.position[1]

    # method to set the score to a certain value
    def set_score(self, score):
        self.score = score

    # method to set the distance to a certain value
    def set_distance(self, distance):
        self.distance = distance

    # method to get the current distance
    def get_distance(self):
        return self.distance

    # method to get the current score
    def get_score(self):
        return self.score

    # method to get the current position
    def get_position(self):
        return self.position

    # assign the GridElement used to reach this GridElement
    def set_parent(self, parent):
        self.parent = parent
        if parent.distance is not None:
            self.distance = parent.distance+1

    # draw the GridElement
    def draw_grid_element(self, surface):
        compass = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # The four directions
        for neighbour in self.neighbours:
            if self.direction(neighbour) in compass:
                compass.remove(self.direction(neighbour))

        for direction in compass:
            if direction == (0, -1):  # North
                draw.line(surface, (255, 255, 255), (self.position[0] * self.size[0], self.position[1] * self.size[1]),
                           ((self.position[0] + 1) * self.size[0], self.position[1] * self.size[1]), 6)
            if direction == (1, 0):  # East
                draw.line(surface, (255, 255, 255), ((self.position[0] + 1) * self.size[0], self.position[1] * self.size[1]),
                          ((self.position[0] + 1) * self.size[0], (self.position[1] + 1) * self.size[1]), 6)
            if direction == (0, 1):  # South
                draw.line(surface, (255, 255, 255), (self.position[0] * self.size[0], (self.position[1] + 1) * self.size[1]),
                          ((self.position[0] + 1) * self.size[0], (self.position[1] + 1) * self.size[1]), 6)
            if direction == (-1, 0):  # West
                draw.line(surface, (255, 255, 255), (self.position[0] * self.size[0], self.position[1] * self.size[1]),
                          (self.position[0] * self.size[0], (self.position[1] + 1) * self.size[1]), 6)

        # This draw an arrow to from the parent, but in our game we dont want such spoilers so we commented it, but for testing purposes it could be uncommented
        # if self.parent is not None:
        #
        #     vector = self.direction(self.parent)
        #
        #     center = ((self.position[0]+0.5) * self.size[0],(self.position[1]+0.5) * self.size[1])
        #
        #     if vector[0] !=0:
        #         left_point = (center[0]+(vector[0]-vector[1])*self.size[0]/5,center[1]+(vector[1]-vector[0])*self.size[0]/5)
        #         right_point = (center[0] + (vector[0] - vector[1]) * self.size[0] / 5, center[1] + (vector[1] + vector[0]) * self.size[0] / 5)
        #     else:
        #         left_point = (center[0] + (vector[0] - vector[1]) * self.size[0] / 5,
        #                       center[1] + (vector[1] + vector[0]) * self.size[0] / 5)
        #         right_point = (center[0] + (vector[0] + vector[1]) * self.size[0] / 5,
        #                        center[1] + (vector[1] + vector[0]) * self.size[0] / 5)
        #     draw.polygon(surface, (100,100,100),(center,left_point,right_point))
        #     entry_point= (center[0]+vector[0]*self.size[0]/2,center[1]+vector[1]*self.size[1]/2)
        #     end_point = (center[0] + vector[0] * self.size[0] / 5, center[1] + vector[1] * self.size[1] / 5)
        #     draw.line(surface, (100,100,100),end_point,entry_point,int(self.size[0]/20)+1)

    # method to print all the neighbouring nodes
    def print_neighbours(self):

        directions = []
        for neighbor in self.neighbours:
            if self.direction(neighbor) == (0, -1):  # North
                directions.append("North")
            elif self.direction(neighbor) == (1, 0):  # East
                directions.append("East")
            elif self.direction(neighbor) == (0, 1):  # South
                directions.append("South")
            elif self.direction(neighbor) == (-1, 0):  # West
                directions.append("West")
            else:
                directions.append(self.direction(neighbor))

        print(directions)
        return None

    # method to print all the walls
    def print_walls(self):
        # discard the directions where neighbours are
        compass = {(0, -1): "North",
                   (1, 0): "East",
                   (0, 1): "South",
                   (-1, 0): "West"}  # The four directions
        for neighbor in self.neighbours:
            compass.pop(self.direction(neighbor))

        print(list(compass.values()))
        return None
