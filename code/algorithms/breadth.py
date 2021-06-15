from code.classes.board import Board
from code.classes.car import Car
from code.classes.board_BF2 import Board_BF2
from code.classes.car_BF2 import Car_BF2
import queue
import copy
import random

class Breadth_first:

    def __init__(self, board):
        self.start_board = board
        self.q = queue.Queue()
        self.archive = {}

        self.start_board.id = 0
        self.q.put(self.start_board)
        self.archive[self.start_board.id] = self.start_board.matrix

        self.matrix_id = 1
        # self.max_depth = 1000
    

    # def max_depth_reached(self, state):
    #     """
    #     Terminates run if maximum depth is reached.
    #     """
    #     if state.depth == self.max_depth:
    #         print(f'No solution in {max_depth - 1} moves.')
    #         return True

    #     return False
    

    def found_solution(self, state):
        """
        Terminates run if the board is a solution.
        """
        print('SOLUTION FOUND!!')
        state.print()
        for move in state.bf_moves:
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
                child.bf_moves.append([car,move])
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

            # track the depth your currently on
            # if state.depth > depth:
            #     depth = state.depth
            #     print(f'ID: {state.id}\nDepth: {depth}\n')

            # if self.max_depth_reached(state):
            #     break

            children = self.make_children(state)
            winner = self.log_children(children)

            if winner != None:
                #print('SOLUTION FOUND!!')
                break

        return winner.bf_moves

        # if winner != None:
        #     #self.start_board.print()
        #     print(f'ID: {winner.id}')
        #     print(f'depth: {winner.depth}')
        #     print()

        #     for move in winner.bf_moves:
        #         print(move)

#########################################################################################################################

class Breadth_first_V2:

    def __init__(self, board):
        self.start_board = board
        self.q = queue.Queue()
        self.archive = {}

        self.start_board.id = 0
        self.q.put(self.start_board)
        self.archive[self.start_board.id] = self.start_board.matrix

        self.matrix_id = 1


    def make_children(self, state):
        """
        Makes all possible children of a board.
        """
        children = []
        for car in list(state.cars.values()):
            for move in state.get_possibilities(car):
                child = state.copy()
                child.update_matrix(car, move)
                child.moves.append((car,move))
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

            self.q.put(child)
            self.archive[child.id] = child.matrix
        
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
                #print('SOLUTION FOUND!!')
                break

        return winner.moves

#########################################################################################################################

class Breadth_first_Hillclimber(Breadth_first_V2):

    def __init__(self, start_board, finish_board):
        self.start_board = start_board
        self.finish_board = finish_board
        self.q = queue.Queue()
        self.archive = {}

        self.start_board.id = 0
        self.q.put(self.start_board)
        self.archive[self.start_board.id] = self.start_board.matrix

        self.matrix_id = 1
    

    def log_children(self, children):
        """
        Logs all children whose matrix is not in the archive. Returns child if it is the solution.
        """
        for child in children:
            if child.matrix in self.archive.values():
                continue

            child.id = self.matrix_id
            self.matrix_id += 1

            if self.check_finish(child.matrix):
                return child

            self.q.put(child)
            self.archive[child.id] = child.matrix
        
        return None

    
    def check_finish(self, matrix):
        """
        Checks if finish matrix has been found.
        """
        for i in range(self.finish_board.board_len):
            for j in range(self.finish_board.board_len):
                if matrix[i][j] != self.finish_board.matrix[i][j]:
                    return False
        
        return True


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

        del winner.moves[0]

        return winner.moves

#############################################################################################################################

class Breadth_first_beam(Breadth_first_V2):

    def make_children(self, state, beam_width):
        """
        Makes 3 possible children of a board.
        """
        children = []
        
        for i in range(beam_width):
            while True:
                car = random.choice(list(state.cars.values()))
                car_moves = state.get_possibilities(car)

                if len(car_moves) > 0:
                    break
            
            move = random.choice(car_moves)

            child = state.copy()
            child.update_matrix(car, move)
            child.moves.append((car,move))
            children.append(child)

        return children

    def run(self, beam_width):
        """
        Goes breadth first through all possible moves until a solution was found or the maximum depth was reached.
        """
        count = 0
        print
        while not self.q.empty():
            if count % 3 == 0:
                print(round(count / 3, 0))
            count += 1
            state = self.q.get()

            children = self.make_children(state, beam_width)
            winner = self.log_children(children)

            if winner != None:
                #print('SOLUTION FOUND!!')
                break

        if winner == None:
            return None

        return winner.moves
