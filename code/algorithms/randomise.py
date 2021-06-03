import random
import time


def random_move(board):
    """
    Pick random car and make a legal move.
    """
    random_car_possibilities = []

    while len(random_car_possibilities) == 0:
        # pick random car
        random_car = random.choice(list(board.cars.values()))

        # get possibilities
        random_car_possibilities = random_car.get_possibilities(board)

    # make random move
    random_move = random.choice(random_car_possibilities)
    board.update_matrix(random_move, random_car)
    
    return [random_car.car_id, random_move]


def run(board):
    """
    Make random moves until the board is solved.
    """
    moves_made = [['car', 'move']]
    
    counter = 0

    while not board.is_solution():
        move = random_move(board)
        moves_made.append(move)
        # print(moves_made)
        # print('')
        # board.print()
        # print('')
        counter += 1   
    
    # print(counter)
    # board.print()

    return moves_made
 