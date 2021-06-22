from code.classes.board_v3 import Board
from code.classes.car_v3 import Car
import queue

class Breadth_first:
    """
    A breath first approach to solving a rush hour game.
    """
    def __init__(self, model):
        self.start = model
        self.q = queue.Queue()
        self.q.put(self.start)
        self.archive = set()
        self.archive.add(self.start.get_tuple())


    def make_children(self, state):
        """
        Makes all possible children of a board.
        """
        children = []
        cars = state.get_cars()
        for car in cars:
            for move in state.get_possibilities(car):
                child = state.copy()
                child.update_matrix(car, move)
                child.add_move(car.cid, move)
                children.append(child)
        
        return children
    

    def log_children(self, children):
        """
        Logs all children whose matrix is not in the archive. Returns True if a child is a solution.
        """
        for child in children:

            child_tuple = child.get_tuple()
            if child_tuple in self.archive:
                continue

            if child.is_solution():
                return child

            self.q.put(child)
            self.archive.add(child_tuple)
        
        return None


    def run(self):
        """
        Goes breadth first through all possible moves until a solution was found or the maximum depth was reached.
        """
        while not self.q.empty():
            state = self.q.get()

            children = self.make_children(state)
            winner = self.log_children(children)

            if winner != None:
                break

        return winner.moves

class Breadth_first_hillclimber(Breadth_first):

    def __init__(self, start_model, closed_archive_dict):
        self.start = start_model.copy()
        self.finish_boards = closed_archive_dict
        self.q = queue.Queue()
        self.q.put(self.start)
        self.archive = {}
        self.archive[self.start.get_tuple()] = len(self.start.moves)
        self.found = {}
    

    def log_children(self, children):
        """
        Logs all children whose matrix is not in the archive. Returns child if it is the solution.
        """
        for child in children:

            child_tuple = child.get_tuple()
            if child_tuple in self.archive:
                continue

            found_depth = self.check_finish(child)
            if found_depth != None:
                self.found[child_tuple] = (found_depth, child)

            self.q.put(child)

            self.archive[child_tuple] = len(child.moves)

    
    def check_finish(self, child):
        """
        Checks archive for same matrix further along the path.
        """
        matrix = child.get_tuple()

        if matrix in self.finish_boards and len(child.moves) < self.finish_boards[matrix]:
            
            return self.finish_boards[matrix]
        return None


    def run(self, max_depth):
        """
        Goes breadth first through all possible moves until a solution was found or the maximum depth was reached.
        """
        start_depth = len(self.start.moves)

        while not self.q.empty():
            state = self.q.get()

            if len(state.moves) == start_depth + max_depth:
                break

            children = self.make_children(state)
            self.log_children(children)

        min_depth = 0
        winner = None
        for contender in self.found.values():
            if contender[0] > min_depth:
                min_depth = contender[0]
                winner = contender[1]

        if winner != None:
            good_moves = []
            for move in winner.moves[start_depth:]:
                good_moves.append(move)
            return good_moves
        
        return None