import random
import copy
import time

def backtracking_move(board):
    """
    Pick random car and make a legal move that does not lead to a previous state.
    """
    possibilities = []

    while True:
        # pick random car
        random_car = random.choice(list(board.cars.values()))
        
        # check if this car has legal moves
        if random_car.has_legal_moves(board):
            # get possibilities
            possibilities = random_car.get_possibilities(board)
            # print(random_car.car_id)
            # print(f"column = {random_car.column} and row = {random_car.row}")
            # print(possibilities)
            while True:
                # make random move
                random_move = random.choice(possibilities)
                # print(random_move)
                possibilities.remove(random_move)
                # print(possibilities)
                copied_board = copy.deepcopy(board)
                copied_board.update_matrix(random_move, copied_board.cars[random_car.car_id])
                # copied_board.print()
                # print(copied_board.previous_states[0][:][:])
                # print(len(copied_board.previous_states))
                # print()
                if copied_board.matrix not in board.previous_states:
                    # print("True")
                    check = True
                    break

                elif not possibilities:
                    # print("False")
                    check = False
                    break

            if check:
                break
  
    # board.print()
    # print(random_move)
    # print(f"column = {random_car.column} and row = {random_car.row}")
    board.update_matrix(random_move, random_car)
    # board.print()
    # time.sleep(10)
    
    return [random_car.car_id, random_move]


def run(board):
    """
    Make random moves until the board is solved.
    """
    moves_made = [['car', 'move']]
    
    counter = 0

    while not board.is_solution():
        move = backtracking_move(board)
        moves_made.append(move)
        counter += 1
    
    # print(counter)
    # board.print()

    return counter
    