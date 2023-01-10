import bisect
from pygame import *

class Search:

    def __init__(self, graph, screen):
        self.screen = screen
        self.graph = graph
        self.x = -50
        self.y = -50
        self.drawing_path = False
        self.x_coordinates = []
        self.y_coordinates = []
        self.timer = 0
        self.drawing_speed = 20

    def draw_path(self):
        if self.drawing_path is True:
            self.move_to_target()

    def a_star_search(self):
        self.graph.reset_state()                                                                    # reset the graph

        priority_queue = [self.graph.start]                                                         # add the starting node to the priority queue
        visited = []                                                                                # create an empty list of visited nodes

        while len(priority_queue) > 0:                                                              # while the priority queue is not empty
            current_node = priority_queue.pop(0)                                                    # the current node is the first node of the priority queue
            if current_node != self.graph.target and current_node not in visited:
                visited.append(current_node)                                                        # add the current node to the visited nodes
                neighbours = current_node.get_neighbours()                                          # get the neighbours
                for next_node in neighbours:                                                        # for all neighbouring nodes of the current node
                    if next_node not in visited:
                        new_distance = current_node.get_distance()+1                                #calculate the fscore (the new distance)
                        new_score = new_distance+next_node.manhattan_distance(self.graph.target)    #the new score is the fscore plus gscore (the manhattan distance)

                        if next_node not in priority_queue:                                         # if the neighbouring node is not in the priority queue
                            next_node.set_parent(current_node)                                      # set the current node to be their parent
                            next_node.set_score(new_score)                                          # the score of the neighbouring node is the new score
                            bisect.insort_left(priority_queue, next_node)                           # insert the neighbouring node into the priority queue
                        elif new_distance < next_node.get_distance():                               # else if the the new distance is smaller than the current distance of the neighbouring node
                            next_node.set_parent(current_node)                                      # set the current node to be their parent
                            next_node.set_score(new_score)                                          # the score of the neighbouring node is the new score
                            priority_queue.remove(next_node)                                        # we changed the score of the neighbour so we have to remove it and add it again to get it in the right position in the list
                            bisect.insort_left(priority_queue, next_node)                           # after removing, insert the neighbouring node into the priority queue

            else:
                break

        print("The number of visited nodes is: {}".format(len(visited)))
        self.store_found_path()                                                                       # Compute the path , back to front

    def store_found_path(self):
        # Compute the path, back to front.
        current_node = self.graph.target.parent
        self.final_path = []

        while current_node is not None and current_node != self.graph.start:
            current_node = current_node.parent
            self.final_path.append(str(current_node))

        result_1 = [item.split('), ', 1)[0] for item in self.final_path]
        result_2 = [item.split('(', 1)[1] for item in result_1]
        result_3 = [item.split(', ', 1)[0] for item in result_2]
        result_4 = [item.split(', ', 1)[1] for item in result_2]
        self.x_coordinates = [eval(i) for i in result_3]
        self.y_coordinates = [eval(i) for i in result_4]
        self.x_coordinates.reverse()
        self.y_coordinates.reverse()

        self.drawing_path = True

        print("Path length is: {}".format(self.graph.target.distance))

    def move_to_target(self):
        if self.timer % self.drawing_speed is 0:
            self.x = self.x_coordinates[0]*20
            self.y = self.y_coordinates[0]*20

            if len(self.x_coordinates) > 1:
                self.x_coordinates.pop(0)
                self.y_coordinates.pop(0)
            else:
                self.drawing_path = False

        draw.rect(self.screen, (10, 11, 12), Rect(self.x, self.y, 20, 20))

        self.timer += 1

