from code.classes.board import Board
from code.classes.car import Car
import queue
import copy

class Breadth_first:

    def __init__(self, board):
        self.start_board = board
        self.q = queue.Queue()
        self.archive = {}

        self.start_board.id = 0
        self.q.put(self.start_board)
        self.archive[self.start_board.id] = self.start_board.matrix

        self.matrix_id = 1
        self.max_depth = 1000
    

    def max_depth_reached(self, state):
        """
        Terminates run if maximum depth is reached.
        """
        if state.depth == self.max_depth:
            print(f'No solution in {max_depth - 1} moves.')
            return True

        return False
    

    def found_solution(self, state):
        """
        Terminates run if the board is a solution.
        """
        print('SOLUTION FOUND!!')
        state.print()
        for move in state.moves:
            print(move)


    def make_children(self, state):
        """
        Makes all possible children of a board.
        """
        children = []
        for car in list(state.cars.values()):
            for move in car.get_possibilities(state):
                child = copy.deepcopy(state)
                child.update_matrix(move, child.cars[car.car_id])
                child.depth = state.depth + 1
                child.moves.append([car,move])
                children.append(child)
        
        return children

    
    def log_children(self, children):
        """
        Logs all children whose matrix is not in the archive. Returns True if a child is a solution.
        """
        for child in children:
            if child.matrix in self.archive.values():
                    continue

            child.id = self.matrix_id
            self.matrix_id += 1

            if child.is_solution():
                return child

            # if self.found_solution(child):
            #     return True

            self.q.put(child)
            self.archive[child.id] = child.matrix
        
        return None


    def run(self):
        """
        Goes breadth first through all possible moves until a solution was found or the maximum depth was reached.
        """
        depth = 0
        while not self.q.empty():
            state = self.q.get()

            if state.depth > depth:
                depth = state.depth
                print(f'ID: {state.id}\nDepth: {depth}\n')

            if self.max_depth_reached(state):
                break

            children = self.make_children(state)
            winner = self.log_children(children)

            if winner != None:
                print('SOLUTION FOUND!!')
                break

        if winner != None:
            #self.start_board.print()
            print(f'ID: {winner.id}')
            print(f'depth: {winner.depth}')
            print()

            for move in winner.moves:
                print(move)

