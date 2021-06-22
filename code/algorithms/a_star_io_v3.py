from code.algorithms import randomise_a_star as ras
from queue import PriorityQueue
import itertools

class A_star:
    """
    An A* algorithm that finds the optimal solution of a rush hour board.
    """

    def __init__(self, start, goal):
        self.start = start
        self.goal = goal
        self.counter = itertools.count(0, -1)

        # initialise the open / closed list
        self.open = PriorityQueue()
        self.open.put((1000, 1000, self.start))

        self.cars = self.start.get_cars()

        self.closed = set()
        self.open_set = set()

    def get_next_state(self):
        """
        Method that gets the board with the lowest score from open
        """
        return self.open.get()[2]

    def heuristic(self, model):
        """   
        Distance to goal: with a given solution from a random algorithm determine the distance of every car to its final position
        """ 
        score = 0

        for car in self.cars:
            row_model, column_model = model.get_car_pos(car)
            row_goal, column_goal = self.goal.get_car_pos(car)
            score += abs(row_model - row_goal) + abs(column_model - column_goal)

        return score

    def create_children(self, model):
        """
        Create the children of the current model
        """
        # get current possibilities of all cars on board
        for car in self.start.get_cars():
            car_possibilities = model.get_possibilities(car)

            # for every car loop over its possible moves
            for move in car_possibilities:
                # copy the board of the previous board
                new_model = model.copy()

                # update new model with chosen move
                new_model.update_matrix(car, move)

                # append move made to list of moves to get to incumbent (new) model
                new_model.add_move(car.cid, move)

                # For matrix form, turn list of lists into tuple of tuples, such that matrix is hashable
                matrix_tuple = new_model.get_tuple()

                # if this model has not been reached put it on the stack
                if (matrix_tuple not in self.closed) and (matrix_tuple not in self.open_set):
                    new_model.score = len(new_model.moves) + self.heuristic(new_model)
                    self.open.put((new_model.score, next(self.counter), new_model))
                    self.open_set.add(matrix_tuple)


    def run(self):
        counter = 0
        while True:
            state = self.get_next_state()
            counter += 1
            # stop loop if a solution is found
            if self.heuristic(state) == 0:
                print(counter)
                break

            # save states to archive
            self.closed.add(state.get_tuple())

            # create children
            self.create_children(state)      

        return state.moves


    def run_hillclimber(self, max_val):
        counter = 0
        while True:
            state = self.get_next_state()
            counter += 1
            # stop loop if a solution is found
            if self.heuristic(state) == 0:
                # print(counter)
                return state
            
            if counter > max_val:
                return None

            # save states to archive
            self.closed.add(state.get_tuple())

            # create children
            self.create_children(state)    