import copy
from code.algorithms import randomise_a_star as ras

class A_star:
    """
    An A* algorithm that finds the optimal solution of a rush hour board.
    """

    def __init__(self, board):
        self.board = board
        self.solution_board = copy.deepcopy(self.board)

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
        # len_board = float("inf")
        next_state = None
        for board in self.open.values():
            # if board.score > lowest_score:
            #     continue
            if board.score < lowest_score:
                lowest_score = board.score
                next_state = tuple([tuple(i) for i in board.matrix])
                # len_board = len(board.moves)
            # elif board.score == lowest_score and len(board.moves) < len_board:
            #     next_state = tuple([tuple(i) for i in board.matrix])
            #     len_board = len(board.moves)

        return self.open.pop(next_state)
    
    # def get_next_state(self):
    #     """
    #     Get the next state based on multiple heuristics
    #     """
    #     lowest_score = float('inf')
    #     # lowest_score_two = float('inf')
    #     # lowest_score_three = float('inf')
    #     # lowest_score_four = float('inf')
    #     next_state = None

    #     for board in self.open.values():
    #         if board.score > lowest_score:
    #             continue
    #         elif board.score < lowest_score:
    #             lowest_score = board.score
    #             next_state = tuple([tuple(i) for i in board.matrix])
    #         # elif board.score_three < lowest_score_three:
    #         #     lowest_score_three = board.score_three
    #         #     next_state = tuple([tuple(i) for i in board.matrix])
    #         # elif board.score_two < lowest_score_two:
    #         #     lowest_score_two = board.score_two
    #         #     next_state = tuple([tuple(i) for i in board.matrix])
    #         # elif board.score_four < lowest_score_four:
    #         #     lowest_score_four = board.score_four
    #         #     next_state = tuple([tuple(i) for i in board.matrix])
            
            
    #     return self.open.pop(next_state)

    def calculate_h1_score(self, state):
        """
        Heuristic based on the distance of the red car to the exit
        """
        return state.board_len - 2 - state.cars["X"].column

    def calculate_h2_score(self, state):
        """
        Blockers: Heuristic based on the number of cars in the row of the winning car
        """
        filled_spots = 0
    
        for column in state.matrix[state.cars["X"].row]:
            if column is not None:
                filled_spots += 1

        return filled_spots

    def calculate_h3_score(self, state):
        """
        BlockersLowerBound: Heuristic based on heuristic 2 plus the minimum number of cars that block these cars
        """
        score = 0

        for l in range(state.cars["X"].column + 2, state.board_len):
            up_score = 0
            down_score = 0

            if state.matrix[state.cars["X"].row][l] is not None:
                up_set = set()
                down_set = set()

                for k in range(state.board_len):
                    if k <= state.cars["X"].row:
                        up_set.add(state.matrix[k][l])
                    elif k >= state.cars["X"].row:
                        down_set.add(state.matrix[k][l])

                for j in down_set:
                    if j is not None:
                        down_score += 1

                for j in up_set:
                    if j is not None:
                        up_score += 1
                
                score += min(up_score, down_score)

        return score

    def calculate_h4_score(self, old_board, state):
        """
        MoveFreed: checks if the last move increased the number of vehicles free to move
        """
        score = 0

        old_board_moves = 0
        for car in old_board.cars.values():
                car_possibilities = car.get_possibilities(state)

                # for every car loop over its possible moves
                for move in car_possibilities:
                    old_board_moves += 1

        current_board_moves = 0
        for car in state.cars.values():
            car_possibilities = car.get_possibilities(state)

            # for every car loop over its possible moves
            for move in car_possibilities:
                current_board_moves += 1

        score = current_board_moves - old_board_moves
        return score

    def calculate_h5_score(self, state):
        """   
        Distance to goal: with a given solution from a random algorithm determine the distance of every car to its final position
        """ 
        score = 0

        for id in self.solution_board.cars.keys():
            score += abs(state.cars[id].row - self.solution_board.cars[id].row) + abs(state.cars[id].column - self.solution_board.cars[id].column)

        return score

    def calculate_h6_score(self, state):
        """   
        Steps from source: the number of steps from the begin board to the current board.
        """  
        
        return len(state.moves)

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
                    new_board.score = len(new_board.moves) + self.calculate_h3_score(new_board)
                    # new_board.score_two = self.calculate_h4_score(state, new_board)
                    # new_board.score_three = self.calculate_h5_score(new_board)
                    # new_board.score_four = self.calculate_h6_score(new_board)
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

        # get the solution state with a random algorithm
        # randomise = ras.randomise(self.solution_board)
        # randomise.run()
        # self.solution_board.print()
        
        # counter = 0
        # repeat untill a solution is found or no solution is possible
        while True:
            # counter += 1
            # take the board at the top of the stack
            state = self.get_next_state()

            # stop loop if a solution is found
            if state.is_solution():
                break

            # save states to archive
            self.closed[tuple([tuple(i) for i in state.matrix])] = state

            # create children
            self.create_children(state)

        # state.print()

        # check if a faster set of moves was possible to get to states in the solution
        solution = self.move_backtracking(state)
        # print(counter)
        

        return solution
