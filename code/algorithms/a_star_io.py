from queue import PriorityQueue
import itertools

class A_star:
    """
    An A* algorithm that finds the shortest path between two given rush hour configurations.
    """

    def __init__(self, start, goal):
        # save the start and goal model
        self.start = start
        self.goal = goal

        # initialise the priority queue 
        self.open = PriorityQueue()
        self.open.put(self.start)
        self.counter = itertools.count(0, -1)

        # initialise archives
        self.closed = set()
        self.open_set = set()

        # load the list of cars
        self.cars = self.start.get_cars()

    def get_next_state(self):
        """
        Method that gets the board with the lowest score from open
        """
        return self.open.get()

    def heuristic(self, model):
        """   
        Distance to goal: with a given goal board determine how many cars are not on its final position.
        """ 
        score = 0

        # check if car is in goal position: if not, increment heuristic score by 1
        for car in self.cars:
            row_model, column_model = model.get_car_pos(car)
            row_goal, column_goal = self.goal.get_car_pos(car)
            if abs(row_model - row_goal) > 0 or abs(column_model - column_goal) > 0: 
                score += 1

        return score

    def create_children(self, model):
        """
        Create the children of the current model
        """
        # get current possibilities of all cars on board
        for car in self.start.get_cars():
            car_possibilities = model.get_possibilities(car)
            for move in car_possibilities:
                new_model = model.copy()
                new_model.update_matrix(car, move)
                new_model.add_move(car.cid, move)

                # Make matrix hashable
                matrix_tuple = new_model.get_tuple()

                # if this model has not been reached put it in the priority queue
                if (matrix_tuple not in self.closed) and (matrix_tuple not in self.open_set):
                    new_model.score = len(new_model.moves) + self.heuristic(new_model)
                    new_model.fifo_score = next(self.counter)
                    self.open.put(new_model)
                    self.open_set.add(matrix_tuple)

    def run(self, max_val):
        """
        Run the A* IO till a path from the start board to the goal board is found.
        """
        counter = 0

        solution_found = False

        # do-while loop that runs untill the the goal board is found
        while not solution_found:
            state = self.get_next_state()
            
            if self.heuristic(state) == 0:
                solution_found = True
                continue
            
            # limit the amount of states the A* may evaluate (otherwise can run out of memory)
            if counter > max_val:
                return (False, None)

            # save states to archive
            self.closed.add(state.get_tuple())
 
            self.create_children(state)  

            counter += 1  

        return (True, state)