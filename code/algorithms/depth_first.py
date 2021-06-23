class DepthFirst():
    """
    A depth first approach to solving a rush hour game. 
    This algorithm goes depth first through the entire state space below a maximum number of moves by using a stack,
    checking each state for the solution. It is guaranteed to find the best solution if it exists within the maximum
    number of moves. It may take a lot of time for larger state spaces.
    """

    def __init__(self, model):
        self.stack = [model.copy()]
        self.archive = {}
        self.solutions = []


    def get_next_state(self):
        """
        Method that gets the next state from the list of states.
        """
        return self.stack.pop()


    def create_children(self, model):
        """
        Creates all possible children of a board.
        """
        for car in model.get_cars():
            for move in model.get_possibilities(car):
                new_model = model.copy()
                new_model.update_matrix(car, move)
                new_model.add_move(car.cid, move)

                # Turn matrix into hashable tuple for archive key
                matrix_tuple = new_model.get_tuple()

                if matrix_tuple not in self.archive.keys():
                    self.stack.append(new_model)
                    
                # if current matrix already in archive with longer movelist, add current matrix to archive
                elif matrix_tuple in self.archive.keys() and len(new_model.moves) < self.archive.get(matrix_tuple, None):
                    self.stack.append(new_model)


    def run(self, max_depth):
        """
        Goes depth first through all possible moves until a solution was found or the maximum depth has been reached.
        """
        while len(self.stack) > 0:
            state = self.get_next_state()

            if state.is_solution():
                self.solutions.append(state.moves)

            if len(state.moves) < max_depth:
                self.create_children(state)

                self.archive[state.get_tuple()] = len(state.moves)

        # sort solutions best to worst
        self.solutions.sort(key=len)

        if self.solutions:
            return self.solutions[0]

        print("This depth is not sufficient")
        return []