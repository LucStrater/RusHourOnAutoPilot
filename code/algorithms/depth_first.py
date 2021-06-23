class DepthFirst():
    """
    A Depth First algorithm that builds a stack of boards.
    """
    def __init__(self, model):
        self.model = model.copy()

        # initialise the stack with the starting board
        self.stack = [model.copy()]

        self.archive = {}
        self.solutions = []

    def get_next_state(self):
        """
        Method that gets the next state from the list of states.
        """
        # take value 
        return self.stack.pop()

    def create_children(self, model):
        # get current possibilities of all cars on board
        for car in model.get_cars():
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

                # if this state has not been reached put it on the stack
                if matrix_tuple not in self.archive.keys():
                    self.stack.append(new_model)
                    
                # if current matrix exists in archive, and moves to get to current matrix is shorter, add current matrix to archive
                elif matrix_tuple in self.archive.keys() and len(new_model.moves) < self.archive.get(matrix_tuple, None):
                    self.stack.append(new_model)


    def run(self, depth):
        # repeat untill the stack is empty
        while len(self.stack) > 0:
            # take the board at the top of the stack
            state = self.get_next_state()
            # depth = 16

            # if the current board is a solution save it
            if state.is_solution():
                self.solutions.append(state.moves)

            # if length of list of moves is smaller than depth, create new boards at deeper level 
            if len(state.moves) < depth:
                self.create_children(state)

                # save states to archive
                self.archive[state.get_tuple()] = len(state.moves)

        # solutions sorted 
        self.solutions.sort(key=len)

        # return the best solution found
        if self.solutions:
            return self.solutions[0]
        else:
            print("This depth is not sufficient")
            return []