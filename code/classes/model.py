from .board import Board
import copy
import csv

class Model:
    """
    This is a model for a rush hour game following the environment model agent approach.
    """
#======================================= Methods for initializing a model =======================================#    
    def __init__(self, source_file): 
        self.board = Board()
        self.matrix = []
        self.load_matrix(source_file)
        self.moves = [('car', 'move')]
        self.score = 1000
        self.fifo_score = 1


    def load_matrix(self, source_file):
        """
        Initializes the board by loading all vehicles from source file.
        """
        self.board.load_length(source_file)

        # fill matrix with None
        self.matrix = [[None for i in range(self.board.board_len)] for j in range(self.board.board_len)]

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
                
                # initialize winning row
                if car_id == 'X':
                    self.board.load_win_row(car_row)

                # fill matrix with cars
                self.matrix[car_row][car_column] = car_id
                if car_orientation == "H":
                    # initialize car with constant row
                    self.board.load_car(car_id, car_orientation, car_length, car_row)

                    self.matrix[car_row][car_column + 1] = car_id
                    if car_length == 3:
                        self.matrix[car_row][car_column + 2] = car_id
                else:
                    # initialize car with constant column
                    self.board.load_car(car_id, car_orientation, car_length, car_column)

                    self.matrix[car_row + 1][car_column] = car_id
                    if car_length == 3:
                        self.matrix[car_row + 2][car_column] = car_id


#================================== Methods that get information from a model ==================================#
    def get_car_pos(self, car):
        """
        Returns the position of the car in (row, column) format.
        """
        if car.orientation == "H":
            for column in range(self.board.board_len):
                if self.matrix[car.const_pos][column] == car.cid:
                    return (car.const_pos, column)
        else:
            for row in range(self.board.board_len):
                if self.matrix[row][car.const_pos] == car.cid:
                    return (row, car.const_pos)


    def get_possibilities(self, car):
        """
        Returns a list with all legal moves for a car.
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


    def get_cars(self):
        """
        Returns a list of all cars on the board.
        """
        return list(self.board.cars.values())


    def get_tuple(self):
        """
        Gets the tuple of the matrix.
        """
        return tuple([tuple(i) for i in self.matrix])


    def is_solution(self):
        """
        Checks if the current configuration is a solution. 
        """
        if self.matrix[self.board.win_row][self.board.board_len - 1] == 'X':
            return True
        
        return False        


#================================== Methods that alter attributes of a model ==================================#
    def update_matrix(self, car, move):
        """
        Updates the matrix according to a given move.
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
                self.matrix[row][column + move + i] = car.cid
        else:
            # remove car from board
            for i in range(car.length):
                self.matrix[row + i][column] = None

            # place car back on board
            for i in range(car.length):
                self.matrix[row + move + i][column] = car.cid


    def add_move(self, cid, move):
        """
        Adds a move to the board.
        """
        self.moves.append((cid, move))


#===================================== Methods that print and copy a model =====================================#
    def print(self):
        """
        Prints board. 
        """ 
        for row in self.matrix:
            print(row)
        print()


    def copy(self):
        """
        Copies a the board to a child and creates deepcopies of only the matrix and the moves.
        """
        child = copy.copy(self)
        child.matrix = []
        child.moves = []
        
        # fill matrix with None
        child.matrix = [[None for i in range(self.board.board_len)] for j in range(self.board.board_len)]

        # recreate parent matrix
        for i in range(self.board.board_len):
            for j in range(self.board.board_len):
                child.matrix[i][j] = self.matrix[i][j]
        
        # recreate parent moves
        for move in self.moves:
            child.moves.append(move)
        
        return child


#======================================= Methods for comparing two models =======================================#
    def __lt__(self, obj):
        """
        Function evaluating less than (<) for the priority queue.
        """
        return self.score < obj.score or (self.score == obj.score and self.fifo_score < obj.fifo_score)


    def __le__(self, obj):
        """
        Function evaluating less than or equal (<=) for the priority queue.
        """
        return self.score <= obj.score or (self.score == obj.score and self.fifo_score <= obj.fifo_score)


    def __eq__(self, obj):
        """
        Function evaluating equal (==) for the priority queue.
        """
        return self.score == obj.score and self.fifo_score == obj.fifo_score


    def __ne__(self, obj):
        """
        Function evaluating not equal (!=) for the priority queue.
        """
        return self.score != obj.score and self.fifo_score != obj.fifo_score


    def __gt__(self, obj):
        """
        Function evaluating greater than (>) for the priority queue.
        """
        return self.score > obj.score or (self.score == obj.score and self.fifo_score > obj.fifo_score)


    def __ge__(self, obj):
        """
        Function evaluating greater than or equal (>=) for the priority queue.
        """
        return self.score >= obj.score or (self.score == obj.score and self.fifo_score >= obj.fifo_score)
        