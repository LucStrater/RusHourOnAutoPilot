from .depth_first import DepthFirst
import copy

class Iterative_deepening(DepthFirst):

    def run(self):
        depth = 1

        while not self.solutions:
            self.stack = [copy.deepcopy(self.board)]
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
                    self.archive[tuple([tuple(i) for i in state.matrix])] = len(state.moves)
            
            # print(f"Depth {depth} is done")
            depth += 1

        # return the best solution found
        return self.solutions[0]
