import random
from code.algorithms import randomise



# def red_car(board):
#     """
#     Check if red car can be moved right.
#     """
#     red_car = board.cars['X']
#     possibilities = red_car.get_possibilities(board)

#     if len(possibilities) > 0:
#         for i in range(len(possibilities)):
#             if possibilities[i] > 0:
#                 return True
    
#     return False


# def red_car_move(board):
#     """
#     Move red car to the right as much as possible.
#     """
#     red_car = board.cars['X']
#     possibilities = red_car.get_possibilities(board)

#     board.update_matrix(max(possibilities), red_car)


def finish(board):
    """
    Check if red car can be moved to solution state.
    """
    red_car = board.cars['X']
    possibilities = red_car.get_possibilities(board)

    for move in possibilities:
        if red_car.column + move == board.board_len - 2:
            return True
    
    return False


def finish_move(board):
    """
    Move red car to solution state.
    """
    red_car = board.cars['X']
    possibilities = red_car.get_possibilities(board)
    win_move = board.board_len - 2 - red_car.column

    if win_move in possibilities:
        board.update_matrix(win_move, red_car)
        return [red_car, win_move]
    else:
        print('something is wrong')
        print('')
        board.print()
        print('')
        return randomise.random_move(board)


# def blocking_car_move(board):
#     pass
    

def run(board):
    """
    Check if greedy move is available and perform it if possible. Otherwhise make random move. 
    Continue until the board is solved.
    """
    moves_made = [['car', 'move']]
    
    counter = 0

    while not board.is_solution():

        if finish(board):
            move = finish_move(board)
        else:
            move = randomise.random_move(board)

        moves_made.append(move)
        counter += 1   

    # return moves_made
    return counter


def print_last_steps(board, moves_by_cars):
    last_moves = moves_by_cars[-3:]
    print(last_moves)

    for i in reversed(range(len(last_moves))):
        print('')
        board.print()
        print('')
        move_by_car = last_moves[i]
        print(move_by_car)
        
        board.update_matrix(move_by_car[1] * -1, move_by_car[0])
    
    print('')
    board.print()

