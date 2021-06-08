from code.classes.board import Board
from code.classes.car import Car
import queue
import copy

def run(board):
    """
    
    """
    max_depth = 25
    q = queue.Queue()
    q.put(board)
    
    board.id = 0
    matrix_id = 1

    archive = {}
    archive[board.id] = board.matrix

    move_archive = {}
    moves = []
    
    while not q.empty():
        state = q.get()

        if state.is_solution():
            print('SOLUTION FOUND!!')
            state.print()
            break
        if state.depth == max_depth:
            print(f'No solution in {max_depth - 1} moves.')
            break

        depth = state.depth

        for car in list(state.cars.values()):
            for move in car.get_possibilities(state):

                child = copy.deepcopy(state)
                child.update_matrix(move, child.cars[car.car_id])
                child.depth = depth + 1
                
                if child.matrix in archive.values():
                    continue

                child.id = matrix_id
                matrix_id += 1

                q.put(child)
                archive[child.id] = child.matrix

