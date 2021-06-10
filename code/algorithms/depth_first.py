import copy

class DepthFirst():
    """
    A Depth First algorithm that builds a stack of boards.
    """
    def __init__(self, board):
        self.board = copy.deepcopy(board)

        # initialise the stack with the starting board
        self.stack = [copy.deepcopy(self.board)]

        self.archive = {}
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

                # For matrix form, turn list of lists into tuple of tuples, such that matrix is hashable
                matrix_tuple = tuple([tuple(i) for i in new_board.matrix])

                # if this state has not been reached put it on the stack
                if matrix_tuple not in self.archive.keys():
                    self.stack.append(new_board)
                    
                # if current matrix exists in archive, and moves to get to current matrix is shorter, add current matrix to archive
                elif matrix_tuple in self.archive.keys() and len(new_board.moves) < self.archive.get(matrix_tuple, None):
                    self.stack.append(new_board)


    def run(self):
        # repeat untill the stack is empty
        while len(self.stack) > 0:
            # take the board at the top of the stack
            state = self.get_next_state()
            depth = 22

            # if the current board is a solution save it
            if state.is_solution():
                self.solutions.append(state.moves)
                # print(f"Some solution: {state.moves}. This takes {len(state.moves) - 1} moves.")

            # if length of list of moves is smaller than depth, create new boards at deeper level 
            if len(state.moves) < depth:
                self.create_children(state)

                # save states to archive
                self.archive[tuple([tuple(i) for i in state.matrix])] = len(state.moves)

        # solutions sorted 
        self.solutions.sort(key=len)

        # return the best solution found
        if self.solutions:
            return self.solutions[0]
        else:
            print("This depth is not sufficient")
            return []