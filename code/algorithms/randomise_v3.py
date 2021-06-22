import random

class Randomise():
    """
    A random algorithm to solve rush hour boards
    """
    def __init__(self, model): 
        self.model = model.copy()

    def random_move(self):
        """
        Pick random car and make a legal move.
        """
        random_car_possibilities = []

        while True:
            # pick random car
            random_car = random.choice(list(self.model.get_cars()))

            # check if this car has legal moves
            if self.model.get_possibilities(random_car):
                break

        # get possibilities
        random_car_possibilities = self.model.get_possibilities(random_car)

        # make random move
        random_move = random.choice(random_car_possibilities)
        self.model.update_matrix(random_car, random_move)
        self.model.add_move(random_car.cid, random_move)

    def run(self):
        """
        Make random moves until the board is solved.
        """

        while not self.model.is_solution():
            self.random_move()

        return self.model.moves

    def legal_check(self):
        """
        Make random moves until the board is solved for generating boards.
        """
        counter = 0

        while not self.model.is_solution():
            self.random_move()

            if counter > 50000:
                return False

            counter += 1

        return True
