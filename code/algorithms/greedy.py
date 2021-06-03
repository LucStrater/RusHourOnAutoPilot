import random


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


def red_car(board):
    """
    Check if red car can be moved right. DOESN'T WORK!!
    """
    red_car = board.cars['X']
    possibilities = red_car.get_possibilities(board)

    if len(possibilities) > 0:
        for i in range(len(possibilities)):
            if possibilities[i] > 0:
                return True
    
    return False


def blocking_car_move(board):
    pass
    

def greedy_move(board):
    """
    Move red car to the right as much as possible.
    """
    red_car = board.cars['X']
    possibilities = red_car.get_possibilities(board)

    board.update_matrix(max(possibilities), red_car)


def run(board):
    """
    Check if red car can be moved to the right and do so if possible. Otherwhise make random move. 
    Continue until the board is solved.
    """
    moves_made = [['car', 'move']]
    
    counter = 0

    while not board.is_solution():

        if counter % 10 == 0 and red_car(board):
            move = greedy_move(board)
        else:
            move = random_move(board)

        moves_made.append(move)
        # print(moves_made)
        # print('')
        # board.print()
        # print('')
        counter += 1   
    

    return counter
    # return moves_made