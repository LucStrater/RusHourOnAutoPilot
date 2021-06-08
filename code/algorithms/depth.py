import copy
import time

def depth_run(board):

    # add current board to list
    depth = 14
    stack = []
    stack.append(board)

    solutions = []
    while len(stack) > 0:
        state = stack.pop()

        if state.is_solution():
            solutions.append(state.moves)

        # if length of list of moves is smaller than depth, create new boards at deeper level 
        if len(state.moves) < depth:

            # get current possibilities of all cars on board
            for car in state.cars.values():
                car_possibilities = car.get_possibilities(state)
                
                # for every car loop over its possible moves
                for move in car_possibilities:
                    # copy the board of the previous board
                    new_board = copy.deepcopy(state)

                    # update new board with chosen move
                    new_board.update_matrix(move, new_board.cars[car.car_id])
                    
                    # append move made to list of moves to get to incumbent (new) board
                    new_board.add_move(new_board.cars[car.car_id].car_id, move)
                    stack.append(new_board)

    solutions.sort(key=len)

    return solutions[0]