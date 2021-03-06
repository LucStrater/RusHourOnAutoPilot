from .model import Model
from .board import Board
import code.algorithms.randomise as rd
import random

class Generate(Model):
    """
    This class generates a random model with the dimensions input by the user.
    """

    def __init__(self, board_len): 
        self.board = Board()
        self.matrix = []
        self.moves = [('car', 'move')]
        self.score = 1000
        self.generate_matrix(board_len)
        

    def generate_matrix(self, board_len):
        """
        Generating a random Rush Hour board.
        """
        # get board data
        self.board.board_len = board_len
        self.board.win_row = int(round(board_len / 2)) - 1

        # fill matrix with None
        self.matrix = [[None for i in range(self.board.board_len)] for j in range(self.board.board_len)]

        # place the red car
        X_column = random.randint(0, board_len - 3)
        self.matrix[self.board.win_row][X_column] = "X"
        self.matrix[self.board.win_row][X_column + 1] = "X"
        self.board.load_car('X', 'H', 2, self.board.win_row)

        # possible car ids for on the board
        cids = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AY', 'AZ', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV', 'BW', 'BY', 'BZ']

        # try placing a car on the board n times
        for n in range(1000):
            # generate random car features
            car_id = cids.pop(0)
            car_orientation = random.choice(['H', 'H','V'])
            car_length = random.choice([2, 2, 3])
            if car_orientation == 'H':
                car_column = random.randint(0, board_len - car_length)
                car_row = random.randint(0, board_len - 1)

            if car_orientation == 'V':
                car_column = random.randint(0, board_len - 1)
                car_row = random.randint(0, board_len - car_length)
            
            # check if that car can be placed and if so than place it
            if car_orientation == "H":
                if car_length == 2 and self.matrix[car_row][car_column] == None and self.matrix[car_row][car_column + 1] == None:
                    self.matrix[car_row][car_column] = car_id
                    self.matrix[car_row][car_column + 1] = car_id
                    self.board.load_car(car_id, car_orientation, car_length, car_row)

                elif car_length == 3 and self.matrix[car_row][car_column] == None and self.matrix[car_row][car_column + 1] == None and self.matrix[car_row][car_column + 2] == None:
                    self.matrix[car_row][car_column] = car_id
                    self.matrix[car_row][car_column + 1] = car_id
                    self.matrix[car_row][car_column + 2] = car_id
                    self.board.load_car(car_id, car_orientation, car_length, car_row)

                else:
                    cids.append(car_id)
                    continue
            
            if car_orientation == "V":
                if car_length == 2 and self.matrix[car_row][car_column] == None and self.matrix[car_row + 1][car_column] == None:
                    self.matrix[car_row][car_column] = car_id
                    self.matrix[car_row + 1][car_column] = car_id
                    self.board.load_car(car_id, car_orientation, car_length, car_column)

                elif car_length == 3 and self.matrix[car_row][car_column] == None and self.matrix[car_row + 1][car_column] == None and self.matrix[car_row + 2][car_column] == None:
                    self.matrix[car_row][car_column] = car_id
                    self.matrix[car_row + 1][car_column] = car_id
                    self.matrix[car_row + 2][car_column] = car_id
                    self.board.load_car(car_id, car_orientation, car_length, car_column)

                else:
                    cids.append(car_id)
                    continue

            # check if the board can be solved within a given amount of moves, if so keep this car
            randomise = rd.Randomise(self)
            
            if randomise.legal_check(50000):
                continue

            cids.append(car_id)

            # move was (probably) not legal so remove this car from the board again
            if car_orientation == "H":
                if car_length == 2:
                    self.matrix[car_row][car_column] = None
                    self.matrix[car_row][car_column + 1] = None
                    self.board.cars.pop(car_id)

                elif car_length == 3:
                    self.matrix[car_row][car_column] = None
                    self.matrix[car_row][car_column + 1] = None
                    self.matrix[car_row][car_column + 2] = None
                    self.board.cars.pop(car_id)
            
            if car_orientation == "V":
                if car_length == 2:
                    self.matrix[car_row][car_column] = None
                    self.matrix[car_row + 1][car_column] = None
                    self.board.cars.pop(car_id)

                elif car_length == 3:
                    self.matrix[car_row][car_column] = None
                    self.matrix[car_row + 1][car_column] = None
                    self.matrix[car_row + 2][car_column] = None
                    self.board.cars.pop(car_id)
                    


            



