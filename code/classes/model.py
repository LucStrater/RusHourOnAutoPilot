from .board_v3 import Board
import copy
import csv

class Model:
    """
    This is a model for a rush hour game following the environment model agent approach.
    """
    def __init__(self, source_file): 
        self.board = Board()
        self.matrix = self.load_matrix(source_file)
        self.moves = [('car', 'move')]
        self.score = 1000

    def load_matrix(self, source_file):
        """
        Initialize the board by loading all vehicles from source file.
        """
        # get board length
        self.board.load_length(source_file)

        # fill matrix with None
        self.matrix = [[None for i in range(self.board.board_len)] for j in range(self.board.board_len)]

        # for all cars in the csv file create the car and put on board
        with open(source_file, 'r') as file:
            reader = csv.reader(file)
            file.readline()

            # loop over all the cars in the source file
            for row in reader:
                car_id = row[0]
                car_orientation = row[1]
                car_column = int(row[2]) - 1
                car_row = int(row[3]) - 1
                car_length = int(row[4])
                
                # initialize winning row
                if car_id == 'X':
                    self.board.load_win_row(car_row)
                
                # fill matrix with cars
                self.matrix[car_row][car_column] = car_id
                if car_orientation == "H":
                    # initialize car
                    self.board.load_car(car_id, car_orientation, car_length, car_row)

                    self.matrix[car_row][car_column + 1] = car_id
                    if car_length == 3:
                        self.matrix[car_row][car_column + 2] = car_id
                else:
                    # initialize car
                    self.board.load_car(car_id, car_orientation, car_length, car_column)

                    self.matrix[car_row + 1][car_column] = car_id
                    if car_length == 3:
                        self.matrix[car_row + 2][car_column] = car_id


    def get_car_pos(self, car):
        """
        Return the position of the car in (row, column) format.
        """
        if car.orientation == "H":
            for column in range(self.board.board_len):
                if self.matrix[car.const_pos][column] == car.id:
                    return (car.const_pos, column)
        else:
            for row in range(self.board.board_len):
                if self.matrix[row][car.const_pos] == car.id:
                    return (row, car.const_pos)


    def get_possibilities(self, car):
        """
        Return a list with all legal moves for a car.
        """
        possibilities = []

        position = self.get_car_pos(car)
        row = position[0]
        column = position[1]

        # moves left
        if car.orientation == 'H' and column != 0:
            for i in range(1, column + 1):
                if self.matrix[row][column - i] == None:
                    possibilities.append(-i)
                else:
                    break

        # moves right
        if car.orientation == 'H' and column != self.board.board_len:
            for i in range(car.length, self.board.board_len - column):
                if self.matrix[row][column + i] == None:
                    possibilities.append(i - car.length + 1)
                else:
                    break

        # moves up
        if car.orientation == 'V' and row != 0:
            for i in range(1, row + 1):
                if self.matrix[row - i][column] == None:
                    possibilities.append(-i)
                else:
                    break
        
        # moves down
        if car.orientation == 'V' and column != self.board.board_len:
            for i in range(car.length, self.board.board_len - row):
                if self.matrix[row + i][column] == None:
                    possibilities.append(i - car.length + 1)
                else:
                    break

        return possibilities
        

    def update_matrix(self, car, move):
        """
        Update the matrix according to a given move.
        """
        position = self.get_car_pos(car)
        row = position[0]
        column = position[1]

        if car.orientation == 'H':
            # remove car from board
            for i in range(car.length):
                self.matrix[row][column + i] = None
            # place car back on board
            for i in range(car.length):
                self.matrix[row][column + move + i] = car.id
        else:
            # remove car from board
            for i in range(car.length):
                self.matrix[row + i][column] = None
            # place car back on board
            for i in range(car.length):
                self.matrix[row + move + i][column] = car.id


    def print(self):
        """
        Print board. 
        """ 
        for row in self.matrix:
            print(row)
        print()


    def add_move(self, cid, move):
        """
        Add a move to the board.
        """
        self.moves.append((cid, move))


    def copy(self):
        """
        Copies a the board to a child and creates deepcopies of only the matrix and the moves.
        """
        # Shallow copy with references to board and methods
        child = copy.copy(self)

        # Create new matrix and moves list for child
        child.matrix = []
        child.moves = []
        
        # Fill matrix with None
        child.matrix = [[None for i in range(self.board_len)] for j in range(self.board_len)]

        # Recreate parent matrix
        for i in range(self.board.board_len):
            for j in range(self.board.board_len):
                child.matrix[i][j] = self.matrix[i][j]
        
        # Recreate parent moves
        for move in self.moves:
            child.moves.append(move)
        
        return child


    def is_solution(self):
        """
        Check if the current configuration is a solution. 
        """
        if self.matrix[self.board.win_row][self.board.board_len - 1] == 'X':
            return True
        
        return False        