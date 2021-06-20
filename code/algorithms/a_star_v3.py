from code.algorithms import randomise_a_star as ras
from queue import PriorityQueue
import itertools

class A_star:
    """
    An A* algorithm that finds the optimal solution of a rush hour board.
    """

    def __init__(self, model):
        self.model = model
        self.counter = itertools.count(0, -1)

        # initialise the open / closed list
        self.open = PriorityQueue()
        self.open.put((1000, 1000, self.model))

        self.closed = set()
        self.open_set = set()

    def get_next_state(self):
        """
        Method that gets the board with the lowest score from open
        """
        return self.open.get()[2]

    def calculate_h1_score(self, model):
        """
        Zero Heuristic
        """
        return 0

    def calculate_h2_score(self, model):
        """
        Blockers: Heuristic based on the number of cars in the row of the winning car
        """
        filled_spots = 0
    
        for column in model.matrix[model.get_car_pos(model.board.cars['X'])[0]]:
            if column is not None:
                filled_spots += 1

        return filled_spots

    def calculate_h3_score(self, model):
        """
        BlockersLowerBound: Heuristic based on heuristic 2 plus the minimum number of cars that block these cars
        """
        score = 0

        for index in range(model.get_car_pos(model.board.cars['X'])[1] + 2, model.board.board_len):
            up_score = 0
            down_score = 0

            if model.matrix[model.get_car_pos(model.board.cars['X'])[0]][index] is not None:
                up_set = set()
                down_set = set()

                for k in range(model.board.board_len):
                    if k <= model.get_car_pos(model.board.cars['X'])[0]:
                        up_set.add(model.matrix[k][index])
                    elif k >= model.get_car_pos(model.board.cars['X'])[0]:
                        down_set.add(model.matrix[k][index])

                for j in down_set:
                    if j is not None:
                        down_score += 1

                for j in up_set:
                    if j is not None:
                        up_score += 1
                
                score += min(up_score, down_score)

        return score

    def create_children(self, model):
        """
        Create the children of the current model
        """
        # get current possibilities of all cars on board
        for car in self.model.get_cars():
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
                    score = len(new_model.moves) + self.calculate_h3_score(new_model)
                    self.open.put((score, next(self.counter), new_model))
                    self.open_set.add(matrix_tuple)


    def run(self):
        counter = 0
        while True:
            state = self.get_next_state()
            counter += 1
            # stop loop if a solution is found
            if state.is_solution():
                print(counter)
                break

            # save states to archive
            self.closed.add(state.get_tuple())

            # create children
            self.create_children(state)      

        return state.moves