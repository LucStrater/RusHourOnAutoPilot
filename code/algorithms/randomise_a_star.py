import random

class randomise():
    """
    A random algorithm to solve rush hour boards
    """
    def __init__(self, board): 
        self.board = board

    def random_move(self):
        """
        Pick random car and make a legal move.
        """
        random_car_possibilities = []

        while True:
            # pick random car
            random_car = random.choice(list(self.board.cars.values()))

            # check if this car has legal moves
            if random_car.has_legal_moves(self.board):
                break

        # get possibilities
        random_car_possibilities = random_car.get_possibilities(self.board)

        # make random move
        random_move = random.choice(random_car_possibilities)
        self.board.update_matrix(random_move, random_car)

    def run(self):
        """
        Make random moves until the board is solved.
        """

        while not self.board.is_solution():
            self.random_move()

