import csv
from .car_BF2 import Car_BF2 as Car
import copy

class Board_BF2():

    def __init__(self, source_file):
        self.board_len = int(source_file.strip("./data/input/Rushhour").split('x')[0])
        self.win_row = 0
        self.cars = {}
        self.matrix = []
        self.load_matrix(source_file)
        self.moves = [('Car','Move')]
        self.id = None


    def load_matrix(self, source_file):
        """
        Initialize the board by loading all vehicles from source file.
        """
        # fill board with None
        self.matrix = [[None for i in range(self.board_len)] for j in range(self.board_len)]

        # for all cars in the csv file create the car and put on board
        with open(source_file, 'r') as file:
            reader = csv.reader(file)
            file.readline()

            for row in reader:
                car_id = row[0]
                car_orientation = row[1]
                car_column = int(row[2]) - 1
                car_row = int(row[3]) - 1
                car_length = int(row[4])

                vehicle = Car(row[0], row[1], int(row[4]))
                self.cars[row[0]] = vehicle

                if car_id == 'X':
                    self.win_row = car_row

                self.matrix[car_row][car_column] = car_id
                if car_orientation == "H":
                    self.matrix[car_row][car_column + 1] = car_id
                    if car_length == 3:
                        self.matrix[car_row][car_column + 2] = car_id
                else:
                    self.matrix[car_row + 1][car_column] = car_id
                    if car_length == 3:
                        self.matrix[car_row + 2][car_column] = car_id


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
        if car.orientation == 'H' and column != self.board_len:
            for i in range(car.length, self.board_len - column):
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
        if car.orientation == 'V' and column != self.board_len:
            for i in range(car.length, self.board_len - row):
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
            for i in range(car.length):
                self.matrix[row][column + i] = None
            for i in range(car.length):
                self.matrix[row][column + move + i] = car.id
        else:
            for i in range(car.length):
                self.matrix[row + i][column] = None
            for i in range(car.length):
                self.matrix[row + move + i][column] = car.id


    def get_car_pos(self, car):
        """
        Return the position of the car in [row, column] format.
        """
        for i in range(self.board_len):
            for j in range(self.board_len):
                if self.matrix[i][j] == car.id:
                    return [i, j]


    def is_solution(self):
        """
        Check if the current configuration is a solution. 
        """
        if self.matrix[self.win_row][self.board_len - 1] == 'X':
            return True
        
        return False


    def print(self):
        """
        Print board. 
        """ 
        for row in self.matrix:
            print(row)
        print()


    def copy(self):
        """
        Copies a the board to a child and creates deepcopies of only the matrix and the moves.
        """
        child = copy.copy(self)
        child.matrix = copy.deepcopy(self.matrix)
        child.moves = copy.deepcopy(self.moves)
        
        return child
    
