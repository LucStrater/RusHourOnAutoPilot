import copy
from code.algorithms import randomise_a_star as ras

class A_star:
    """
    An A* algorithm that finds the optimal solution of a rush hour board.
    """

    def __init__(self, model):
        self.model = model

        # initialise the open / closed list
        self.open = {}
        self.open[self.model.get_tuple()] = self.model.copy()

        self.closed = {}
        self.closed[self.model.get_tuple()] = self.model.copy()

    def get_next_state(self):
        """
        Method that gets the board with the lowest score from open
        """
        lowest_score = float("inf")
        next_state = None
        for model in self.open.values():
            if model.score < lowest_score:
                lowest_score = model.score
                next_state = model.get_tuple()

        return self.open.pop(next_state)

    def calculate_h1_score(self, model):
        """
        Heuristic based on the distance of the red car to the exit
        """
        return model.board.board_len - 2 - model.get_car_pos(model.board.cars['X'])[1]

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

    def calculate_h4_score(self, old_model, model):
        """
        MoveFreed: checks if the last move increased the number of vehicles free to move
        """
        score = 0

        old_model_moves = 0
        for car in old_model.get_cars():
            car_possibilities = old_model.get_possibilities(car)

            # for every car loop over its possible moves
            old_model_moves += len(car_possibilities)

        current_model_moves = 0
        for car in model.get_cars():
            car_possibilities = model.get_possibilities(car)

            # for every car loop over its possible moves
            current_model_moves += len(car_possibilities)

        score = current_model_moves - old_model_moves
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
                if (matrix_tuple not in self.closed.keys() and matrix_tuple not in self.open.keys()):
                    new_model.score = len(new_model.moves) + self.calculate_h2_score(new_model)
                    self.open[matrix_tuple] = new_model

                # if current matrix exists in archive, and moves to get to current matrix is shorter, replace model in archive
                elif matrix_tuple in self.closed.keys():
                    if len(new_model.moves) < len(self.closed[matrix_tuple].moves):
                        self.closed[matrix_tuple].moves = new_model.moves

                # same as above, but for open
                elif matrix_tuple in self.open.keys():
                    if len(new_model.moves) < len(self.open[matrix_tuple].moves):
                        self.open[matrix_tuple].moves = new_model.moves

    def move_backtracking(self, solution_model):
        # list with the solution
        optimal_moveset = []

        # do while loop
        while True:
            # take the last element of the move and save it to the solution
            optimal_moveset.insert(0, solution_model.moves.pop())

            # stop if start board is reached
            if solution_model.matrix == self.model.matrix:
                break

            # take the new last move and look if there is a faster route to get there in the archive
            move = -optimal_moveset[0][1]
            car = solution_model.board.cars[optimal_moveset[0][0]]
            solution_model.update_matrix(car, move)
            solution_model.moves = self.closed[solution_model.get_tuple()].moves

        return optimal_moveset

    def run(self):

        while True:
            state = self.get_next_state()

            # stop loop if a solution is found
            if state.is_solution():
                break

            # save states to archive
            self.closed[state.get_tuple()] = state

            # create children
            self.create_children(state)

        # check if a faster set of moves was possible to get to states in the solution
        solution = self.move_backtracking(state)        

        return solution