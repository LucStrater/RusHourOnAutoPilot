from .car_v3 import Car

class Board:
    """
    The board class represents a rush hour board and holds only static data and is part of the environment.
    """
    def __init__(self):
        self.board_len = 0
        self.win_row = 1
        self.cars = {}

    def load_length(self, source_file):
        """
        Load the length of the board.
        """
        self.board_len = int(source_file.strip("./data/input/Rushhour").split('x')[0])

    def load_car(self, cid, orientation, length, const_pos):
        """
        Load the data from the source file for a given board.
        """
        
        self.cars[cid] = Car(cid, orientation, length, const_pos)
        
    def load_win_row(self, row):
        """
        Load winning row.
        """
        self.win_row = row   
        