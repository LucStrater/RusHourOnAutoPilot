import copy

class DepthFirst():
    """
    A Depth First algorithm that builds a stack of boards.
    """
    def __init__(self, board):
        self.board = copy.deepcopy(board)

        # initialise the stack with the starting board
        self.stack = [copy.deepcopy(self.board)]

        self.archive = []
        self.archive_of_boards = []
        self.alternative = {}
        self.solutions = []

    def get_next_state(self):
        """
        Method that gets the next state from the list of states.
        """
        # take value 
        return self.stack.pop()

    def create_children(self, state):
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

                # proofed working but needs to append matrices below
                if new_board.matrix not in self.archive:
                    self.stack.append(new_board)

                # archive_of_boards = []
                # for state in self.archive:
                #     archive_of_boards.append(state.matrix)

                # if new_board.matrix in self.archive:
                #     for board in self.archive_of_boards:
                #         if new_board.matrix == board.matrix:
                #             if len(new_board.moves) < len(board.moves):
                #                 self.stack.append(new_board)
                
                if new_board.matrix in self.archive:
                    tupled_cur_matrix = tuple([tuple(i) for i in new_board.matrix])
                    len_of_existing_board = self.alternative.get(tupled_cur_matrix, None)
                    # print(f"len of existing board: {len_of_existing_board}")
                    if len(new_board.moves) < len_of_existing_board:
                        self.stack.append(new_board)


        self.archive.append(state.matrix)
        # self.archive_of_boards.append(state)

        # len_of_state_board = len(state.moves)
        # print(f"length of state board: {len_of_state_board}")
        # print(f"this is the state.matrix: {state.matrix}")
        tupled_matrix = tuple([tuple(i) for i in state.matrix])
        # print(f"this is the tuple of state.matrix: {tupled_matrix}")
        self.alternative[tupled_matrix] = len(state.moves)


    def run(self):
        # repeat untill the stack is empty
        while len(self.stack) > 0:
            # take the board at the top of the stack
            state = self.get_next_state()
            depth = 100

            # if the current board is a solution save it
            if state.is_solution():
                self.solutions.append(state.moves)
                print(f"Some solution: {state.moves}. This takes {len(state.moves) - 1} moves.")

            # if length of list of moves is smaller than depth, create new boards at deeper level 
            if len(state.moves) < depth:
                self.create_children(state)

        # solutions sorted 
        self.solutions.sort(key=len)

        # return the best solution found
        return self.solutions[0]