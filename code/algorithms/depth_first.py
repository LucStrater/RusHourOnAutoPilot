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
                if new_board.matrix not in self.archive or len(new_board.moves) <  :
                    self.stack.append(new_board)

        self.archive.append(state.matrix)

    def run(self):
        # repeat untill the stack is empty
        while len(self.stack) > 0:
            # take the board at the top of the stack
            state = self.get_next_state()
            depth = 14

            # if the current board is a solution save it
            if state.is_solution():
                self.solutions.append(state.moves)
                print(state.moves)

            # if length of list of moves is smaller than depth, create new boards at deeper level 
            if len(state.moves) < depth:
                self.create_children(state)

        # solutions sorted 
        self.solutions.sort(key=len)

        # return the best solution found
        return self.solutions[0]