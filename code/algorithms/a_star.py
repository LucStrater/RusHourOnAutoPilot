import copy


class A_star:
    """
    An A* algorithm that finds the optimal solution of a rush hour board.
    """

    def __init__(self, board):
        self.board = board

        # initialise the open / closed list
        self.open = {}
        self.open[tuple([tuple(i) for i in self.board.matrix])] = copy.deepcopy(self.board)

        self.closed = {}
        self.closed[tuple([tuple(i) for i in self.board.matrix])] = copy.deepcopy(self.board)

    def get_next_state(self):
        """
        Method that gets the board with the lowest score from open
        """
        lowest_score = float("inf")
        len_board = float("inf")
        next_state = None
        for board in self.open.values():
            current_score = self.calculate_h2_score(board)
            if current_score > lowest_score:
                continue
            elif current_score < lowest_score:
                lowest_score = current_score
                next_state = tuple([tuple(i) for i in board.matrix])
                len_board = len(board.moves)
            elif current_score == lowest_score and len(board.moves) < len_board:
                next_state = tuple([tuple(i) for i in board.matrix])
                len_board = len(board.moves)

        return self.open.pop(next_state)

    def calculate_h1_score(self, state):
        """
        Heuristic based on the distance of the red car to the exit
        """
        return state.board_len - 2 - state.cars["X"].column

    def calculate_h2_score(self, state):
        """
        Heuristic based on the number of cars in the row of the winning car
        """
        filled_spots = 0

        for column in state.matrix[state.cars["X"].row]:
            if  column is not None:
                filled_spots += 1

        return filled_spots

    def calculate_h3_score(self, state):
        """
        Heuristic based on the number of cars blocking the red car and the cars blocking those
        """
        score = 0
        len_board = range(state.board_len)

        # check for cars in the row of the red car and cars blocking those cars
        for i in len_board:
            unique = []
            if (state.matrix[state.cars["X"].row][i] is not None and state.matrix[state.cars["X"].row][i] != "X"):
                for j in len_board:
                    if state.matrix[j][i] is not None and state.matrix[j][i] not in unique:
                        score += 1
                        unique.append(state.matrix[j][i])
        return score

    def create_children(self, state):
        """
        Create the children of the current state
        """
        # get current possibilities of all cars on board
        for car in state.cars.values():
            car_possibilities = car.get_possibilities(state)

            # for every car loop over its possible moves
            for move in car_possibilities:
                # copy the board of the previous board
                new_board = copy.deepcopy(state)

                # update new board with chosen move
                new_board.update_matrix(move, new_board.cars[car.car_id])

                # append move made to list of moves to get to incumbent (new) board
                new_board.add_move(new_board.cars[car.car_id].car_id, move)

                # For matrix form, turn list of lists into tuple of tuples, such that matrix is hashable
                matrix_tuple = tuple([tuple(i) for i in new_board.matrix])

                # if this state has not been reached put it on the stack
                if (matrix_tuple not in self.closed.keys() and matrix_tuple not in self.open.keys()):
                    self.open[matrix_tuple] = new_board

                # if current matrix exists in archive, and moves to get to current matrix is shorter, replace board in archive
                elif matrix_tuple in self.closed.keys():
                    if len(new_board.moves) < len(self.closed[matrix_tuple].moves):
                        self.closed[matrix_tuple] = new_board

                # saem as above, but for open
                elif matrix_tuple in self.open.keys():
                    if len(new_board.moves) < len(self.open[matrix_tuple].moves):
                        self.open[matrix_tuple] = new_board

    def move_backtracking(self, solution_state):
        # list with the solution
        optimal_moveset = []

        # do while loop
        while True:
            # take the last element of the move and save it to the solution
            optimal_moveset.insert(0, solution_state.moves.pop())

            # stop if start board is reached
            if solution_state.matrix == self.board.matrix:
                break

            # take the new last move and look if there is a faster route to get there in the archive
            move = -optimal_moveset[0][1]
            car = solution_state.cars[optimal_moveset[0][0]]
            solution_state.update_matrix(move, car)
            solution_state.moves = self.closed[tuple([tuple(i) for i in solution_state.matrix])].moves

        return optimal_moveset

    def run(self):

        # repeat untill a solution is found or no solution is possible
        while True:
            # take the board at the top of the stack
            state = self.get_next_state()

            # stop loop if a solution is found
            if state.is_solution():
                break

            # save states to archive
            self.closed[tuple([tuple(i) for i in state.matrix])] = state

            # create children
            self.create_children(state)

        # check if a faster set of moves was possible to get to states in the solution
        solution = self.move_backtracking(state)

        return solution
