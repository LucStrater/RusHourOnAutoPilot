from .depth_first import DepthFirst
import copy

class Iterative_deepening(DepthFirst):
    """
    Iterative deepening algorithm for solving rush hour boards.
    This algorithm goes depth first through the entire state space below a certain depth. This depth starts at 0
    and increments by one after each DF run. It is guaranteed to find the best solution. 
    It may take a lot of time for larger state spaces.
    """

    def __init__(self, model):
        self.model = model.copy()
        self.stack = [self.model]
        self.archive = {}
        self.solutions = []


    def run(self):
        """
        Goes depth first through all possible moves until a solution was found or the maximum depth has been reached.
        """
        depth = 1

        while not self.solutions:
            self.stack = [self.model.copy()]
            self.archive = {}

            # repeat untill the stack is empty
            while len(self.stack) > 0:
                state = self.get_next_state()

                # if the current board is a solution save it and stop
                if state.is_solution():
                    self.solutions.append(state.moves)
                    break

                # if length of list of moves is smaller than depth, create new boards at deeper level 
                if len(state.moves) < depth:
                    self.create_children(state)

                    # save states to archive
                    self.archive[state.get_tuple()] = len(state.moves)
            
            depth += 1

        return self.solutions[0]
