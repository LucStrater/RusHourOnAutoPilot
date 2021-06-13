import random
import time
# from code.classes.board_BF2 import Board_BF2
# from code.classes.car_BF2 import Car_BF2


def random_move(board):
    """
    Pick random car and make a legal move.
    """
    random_car_possibilities = []

    while True:
        # pick random car
        random_car = random.choice(list(board.cars.values()))

        # check if this car has legal moves
        if random_car.has_legal_moves(board):
            break

    # get possibilities
    random_car_possibilities = random_car.get_possibilities(board)

    # make random move
    random_move = random.choice(random_car_possibilities)
    board.update_matrix(random_move, random_car)
    
    return [random_car.car_id, random_move]


def run_milestone1(board, print_check):
    """
    Make random moves until the board is solved.
    """
    moves_made = [['car', 'move']]
    
    counter = 0

    while not board.is_solution():
        if counter < 10 and print_check:
            print(f"Step {counter}")
            board.print()
            print()
            time.sleep(1)

        move = random_move(board)
        moves_made.append(move)
        counter += 1

    return [moves_made, counter]

###############################################################################################################################

class Randomize_Hillclimber:
    """
    Randomly makes legal moves until the board is solved. Designed for the V2 data structure BF2.
    """

    def __init__(self, board):
        self.board = board


    def random_choice(self):
        """
        Randomly selects car and returns legal move.
        """
        # select car
        while True:
            car = random.choice(list(self.board.cars.values()))
            car_moves = self.board.get_possibilities(car)

            if len(car_moves) > 0:
                break
        
        move = random.choice(car_moves)

        return (car, move)
    

    def run(self):
        """
        Make random moves until the board is solved.
        """
        while not self.board.is_solution():
            car_move = self.random_choice()

            self.board.update_matrix(car_move[0], car_move[1])

            self.board.moves.append(car_move)
        
        return self.board.moves