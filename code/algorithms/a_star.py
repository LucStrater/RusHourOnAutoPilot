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
            if board.score > lowest_score:
                continue
            elif board.score < lowest_score:
                lowest_score = board.score
                next_state = tuple([tuple(i) for i in board.matrix])
                len_board = len(board.moves)
            elif board.score == lowest_score and len(board.moves) < len_board:
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
            if column is not None:
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

    def calculate_h4_score(self, state):
        """
        Heuristic based on heuristic 2 plus the minimum number of cars that block these cars
        """
        len_board = range(state.board_len)
        x_to_end = range(state.cars["X"].row + state.cars["X"].length, state.board_len)
        
        score = 0
        sub_scores = []
        # level_two_blockers_a = 0
        # level_two_blockers_b = 0

        for i in x_to_end:
            sub_score_a = 0
            sub_score_b = 0
            unique = []
            if (state.matrix[state.cars["X"].row][i] is not None and state.matrix[state.cars["X"].row][i] != "X"):
                score += 1 

                blocking_car = state.cars[state.matrix[state.cars["X"].row][i]]
                blocking_car.length

                # look below the directly blocking car
                for j in range(blocking_car.row + blocking_car.length, state.board_len):
                    if state.matrix[j][i] is not None and state.matrix[j][i] not in unique:
                        sub_score_a += 1
                        unique.append(state.matrix[j][i])
                
                # look above the directly blocking car
                for k in range(0, blocking_car.row):
                    if state.matrix[k][i] is not None and state.matrix[k][i] not in unique:
                        sub_score_b += 1
                        unique.append(state.matrix[k][i])
                print(f"score a: ${sub_score_a}, score b: ${sub_score_b}")
                sub_scores.append(min(sub_score_a, sub_score_b))
                print(f"List with minimum sub_scores: ${sub_scores}")
                        
                        # level_two_blocking_car =  state.cars[state.matrix[j][i]]
                        # orientation_car = level_two_blocking_car.orientation
                        # length_car = level_two_blocking_car.length
                        # row_car = level_two_blocking_car.row
                        # column_car = level_two_blocking_car.column

                        # level_three_blockers = 0
                        # if orientation_car == 'H':
                        #     for k in range(column_car + length_car, state.board_len):
                        #         if state.matrix[j][k] is not None:
                        #             level_three_blockers += 1
                        #             break
                        #     for l in range(0, column_car):
                        #         if state.matrix[j][l] is not None:
                        #             level_three_blockers += 1
                        #             break
                        # if orientation_car == 'V':
                        #     # for looking above row of X
                        #     # for k in range(0, row_car):
                        #     #     if state.matrix[i][k] is not None:
                        #     #         level_three_blockers += 1
                        #     #         break
                        #     for l in range(row_car + length_car, state.board_len)
                        #         if state.matrix[i][k] is not None:
                        #             level_three_blockers += 1
                        #             break        
        
        return (score + min(sub_scores))

    def calculate_h5_score(self, state):
        """
        Heuristic based on the number of cars blocking the red car and the cars blocking those
        """
        score = 0

        for l in range(state.cars["X"].column + 2, state.board_len):
            up_score = 0
            down_score = 0

            if state.matrix[state.cars["X"].row][l] is not None:
                up_set = set()
                down_set = set()

                for k in range(state.board_len):
                    if k <= state.cars["X"].row and state.matrix[k][l] is not None:
                        up_set.add(state.matrix[k][l])
                    elif k >= state.cars["X"].row and state.matrix[k][l] is not None:
                        down_set.add(state.matrix[k][l])

                for j in down_set:
                    if j is not None:
                        down_score += 1

                for j in up_set:
                    if j is not None:
                        up_score += 1
                
                score += min(up_score, down_score)

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
                    new_board.score = self.calculate_h5_score(new_board)
                    self.open[matrix_tuple] = new_board

                # if current matrix exists in archive, and moves to get to current matrix is shorter, replace board in archive
                elif matrix_tuple in self.closed.keys():
                    if len(new_board.moves) < len(self.closed[matrix_tuple].moves):
                        self.closed[matrix_tuple].moves = new_board.moves

                # same as above, but for open
                elif matrix_tuple in self.open.keys():
                    if len(new_board.moves) < len(self.open[matrix_tuple].moves):
                        self.open[matrix_tuple].moves = new_board.moves

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
