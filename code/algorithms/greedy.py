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

######################################### 1. FINISH THE BOARD ####################################################################

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

######################################### 2. MOVE A CAR BLOCKING THE RED #########################################################

def blocking(board):
    """
    Return list of cars that can be moved away from the row of the red car.
    """
    red_car = board.cars['X']
    red_car_row = red_car.row

    row_cars = set()
    for car in board.matrix[red_car_row]:
        if car != None and car != red_car.car_id:
            row_cars.add(board.cars[car])
    
    blocking_cars = []
    for car in row_cars:
        if car.column > red_car.column:
            blocking_cars.append(car)

    movable_cars = []
    for car in blocking_cars:
        possibilities = car.get_possibilities(board)
        if len(possibilities) == 0:
            continue
        else:
            for move in possibilities:
                new_pos = car.row + move
                # moving down
                if new_pos > red_car_row:
                    movable_cars.append(car)
                # moving up
                elif new_pos + car.length - 1 < red_car_row:
                    movable_cars.append(car)

    return movable_cars


def blocking_move(board, cars):
    """
    Moves car away from the row of the red car. Picks random if multiple cars are available.
    """
    red_car = board.cars['X']
    red_car_row = red_car.row

    if len(cars) == 1:
        car = cars[0]
    else:
        car = random.choice(cars)
    
    for move in car.get_possibilities(board):
        new_pos = car.row + move
        # moving down
        if new_pos > red_car_row:
            board.update_matrix(move, car)
            return [car, move]
        # moving up
        elif new_pos + car.length - 1 < red_car_row:
            board.update_matrix(move, car)
            return[car, move]

######################################### 3. MOVE ALL CARS BLOCKING RED ##########################################################  

def blocking_cars(board):
    red_car = board.cars['X']
    red_car_row = red_car.row

    row_cars = set()
    for car in board.matrix[red_car_row]:
        if car != None and car != red_car.car_id:
            row_cars.add(board.cars[car])
    
    blocking_cars = []
    for car in row_cars:
        if car.column > red_car.column:
            blocking_cars.append(car)
    
    return blocking_cars


def movable_cars(board, blocking_cars):
    """
    Return list of cars that can be moved away from the row of the red car.
    """
    red_car = board.cars['X']
    red_car_row = red_car.row

    movable_cars = []
    for car in blocking_cars:
        possibilities = car.get_possibilities(board)
        if len(possibilities) == 0:
            continue
        else:
            for move in possibilities:
                new_pos = car.row + move
                # moving down
                if new_pos > red_car_row:
                    movable_cars.append(car)
                    break
                # moving up
                elif new_pos + car.length - 1 < red_car_row:
                    movable_cars.append(car)
                    break

    return movable_cars


def if_finishable(blocking_cars, movable_cars):
    if len(blocking_cars) == len(movable_cars):
        return True
    return False


def execute_blocked_moves(board, movable_cars):
    red_car = board.cars['X']
    red_car_row = red_car.row
    finishing_moves = []
    for car in movable_cars:
        for move in car.get_possibilities(board):
            # print(f'the move: {move}, by {car}... orientation: {car.orientation}, row: {car.row}, column: {car.column}, length: {car.length}')
            new_pos = car.row + move
            # moving down
            if new_pos > red_car_row:
                board.update_matrix(move, car)
                finishing_moves.append([car, move])
                break
            # moving up
            elif new_pos + car.length - 1 < red_car_row:
                board.update_matrix(move, car)
                finishing_moves.append([car, move])
                break

    return finishing_moves

######################################### SOLVE THE BOARD ##############################################################################

def run_1(board):
    """
    Check if greedy move is available and perform it if possible. Otherwhise make random move. 
    Continue until the board is solved.
    """
    moves_made = [['car', 'move']]
    
    counter = 0

    while not board.is_solution():
        block_cars = blocking_cars(board)
        move_cars = movable_cars(board, block_cars)

        ### 1.
        if finish(board):
            move = finish_move(board)
        else:
            move = randomise.random_move(board)

        moves_made.append(move)
        counter += 1

        # if counter % 10000 == 0:
        #     print(counter)   

    # return moves_made
    return counter


def run_2(board):
    """
    Check if greedy move is available and perform it if possible. Otherwhise make random move. 
    Continue until the board is solved.
    """
    moves_made = [['car', 'move']]
    
    counter = 0

    while not board.is_solution():
        block_cars = blocking_cars(board)
        move_cars = movable_cars(board, block_cars)

        ### 1.
        if finish(board):
            move = finish_move(board)
        ### 3.
        elif if_finishable(block_cars, move_cars):
            # execute all the possible moves for cars to right of red car
            moves = execute_blocked_moves(board, move_cars)
            # print(moves)
            for i in moves:
                moves_made.append(i)
        else:
            move = randomise.random_move(board)

        moves_made.append(move)
        counter += 1

        # if counter % 10000 == 0:
        #     print(counter)   

    # return moves_made
    return counter

def run_3(board):
    """
    Check if greedy move is available and perform it if possible. Otherwhise make random move. 
    Continue until the board is solved.
    """
    moves_made = [['car', 'move']]
    
    counter = 0

    while not board.is_solution():
        block_cars = blocking_cars(board)
        move_cars = movable_cars(board, block_cars)

        ### 1.
        if finish(board):
            move = finish_move(board)
        ### 3.
        elif if_finishable(block_cars, move_cars):
            # execute all the possible moves for cars to right of red car
            moves = execute_blocked_moves(board, move_cars)
            # print(moves)
            for i in moves:
                moves_made.append(i)
        ### 2. 
        elif counter % 10 == 0 and len(blocking(board)) > 0:
            move = blocking_move(board, blocking(board))
        else:
            move = randomise.random_move(board)

        moves_made.append(move)
        counter += 1

        # if counter % 10000 == 0:
        #     print(counter)   

    # return moves_made
    return counter

######################################### RETRACE FIRST STEPS ###################################################################################

def print_first_steps(board, moves_by_cars):
    """
    Print the first three states of the board before solving the board
    """
    first_moves = moves_by_cars[:10]
    print(first_moves)

    for i in range(len(first_moves)):
        print()
        board.print()
        print()
        move_by_car = first_moves[i]
        print(move_by_car)
        
        board.update_matrix(move_by_car[1], move_by_car[0])
    
    print()
    board.print()

