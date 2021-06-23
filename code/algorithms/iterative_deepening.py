from .depth_first import DepthFirst
import copy

class Iterative_deepening(DepthFirst):
    """
    Iterative deepening algorithm for solving rush hour boards.
    """
    def run(self):
        depth = 1

        # run till a solution is found
        while not self.solutions:
            self.stack = [self.model.copy()]
            self.archive = {}

            # repeat untill the stack is empty
            while len(self.stack) > 0:
                # take the board at the top of the stack
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

        # return the best solution found
        return self.solutions[0]
