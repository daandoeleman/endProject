# the class which the ufo class uses to find a path for the enemy

import bisect

class Search:

    def __init__(self, clouds):

        # store the clouds so that we can find a way through them
        self.clouds = clouds

        # two arrays to store the coordinates of the eventually found path
        self.x_coordinates = []
        self.y_coordinates = []

    def a_star_search(self):

        self.clouds.reset_state()                                                                    # reset the graph

        priority_queue = [self.clouds.start]                                                         # add the starting node to the priority queue
        visited = []                                                                                # create an empty list of visited nodes

        while len(priority_queue) > 0:                                                              # while the priority queue is not empty
            current_node = priority_queue.pop(0)                                                    # the current node is the first node of the priority queue
            if current_node != self.clouds.target and current_node not in visited:
                visited.append(current_node)                                                        # add the current node to the visited nodes
                neighbours = current_node.get_neighbours()                                          # get the neighbours
                for next_node in neighbours:                                                        # for all neighbouring nodes of the current node
                    if next_node not in visited:
                        new_distance = current_node.get_distance()+1                                #calculate the fscore (the new distance)
                        new_score = new_distance+next_node.manhattan_distance(self.clouds.target)    #the new score is the fscore plus gscore (the manhattan distance)

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

        # print("The number of visited nodes is: {}".format(len(visited)))

        # store the path that we just found
        self.store_found_path()

    def store_found_path(self):

        # store the parent nodes
        current_node = self.clouds.target.parent

        # an array for the nodes of the final path
        self.final_path = []

        while current_node is not None and current_node != self.clouds.start:
            current_node = current_node.parent
            # store all the parents in a list
            self.final_path.append(str(current_node))

        # do a lot of manipulations to convert the nodes into two lists of coordinates
        result_1 = [item.split('), ', 1)[0] for item in self.final_path]
        result_2 = [item.split('(', 1)[1] for item in result_1]
        result_3 = [item.split(', ', 1)[0] for item in result_2]
        result_4 = [item.split(', ', 1)[1] for item in result_2]
        self.x_coordinates = [eval(i) for i in result_3]
        self.y_coordinates = [eval(i) for i in result_4]
        self.x_coordinates.reverse()
        self.y_coordinates.reverse()

        # let the enemy know that it can start moving along the found path
        self.enemy_move = True
