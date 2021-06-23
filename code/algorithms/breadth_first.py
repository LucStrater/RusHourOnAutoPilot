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
                return (True, child)

            self.q.put(child)
            self.archive.add(child_tuple)
        
        return (False, None)


    def run(self):
        """
        Goes breadth first through all possible moves until a solution was found or the maximum depth was reached.
        """
        while not self.q.empty():
            state = self.q.get()

            children = self.make_children(state)
            found_winner, winner = self.log_children(children)
            
            if found_winner:
                break

        return winner.moves

