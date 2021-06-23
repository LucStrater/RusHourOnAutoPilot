import random

class Randomise():
    """
    A random algorithm to solve rush hour boards. 
    It makes random moves until a solution was found.
    """
    def __init__(self, model): 
        self.model = model.copy()


    def random_move(self):
        """
        Pick random car with legal moves and make a move.
        """
        car_found = False
        while not car_found:
            random_car = random.choice(list(self.model.get_cars()))

            if self.model.get_possibilities(random_car):
                car_found = True
                continue

        possible_moves = self.model.get_possibilities(random_car)
        random_move = random.choice(possible_moves)

        self.model.update_matrix(random_car, random_move)
        self.model.add_move(random_car.cid, random_move)


    def run(self):
        """
        Make random moves until the board is solved.
        """
        while not self.model.is_solution():
            self.random_move()

        return self.model.moves


    def legal_check(self, max_counter):
        """
        Make random moves until the board is solved for generating boards.
        """
        counter = 0

        while not self.model.is_solution():
            self.random_move()

            if counter > max_counter:
                return False

            counter += 1

        return True
