import csv
from .car import Car

class Board():

    def __init__(self, source_file):
        self.board_len = 0  
        self.cars = {}
        self.matrix = self.load_matrix(source_file)
        self.moves = [('car', 'move')]
        self.score = 1000
        self.score_two = 1000
        self.score_three = 1000
        self.score_four = 1000
    #     self.car_possibilities = self.load_possibilities()

    # def load_possibilities(self):
    #     # get starting possibilities of all cars on the initial board
    #     for car in self.cars.values():
    #         car_possibilities = car.get_possibilities(self)

    #         # for every car loop over its possible moves
    #         for move in car_possibilities:        
       
    def load_matrix(self, source_file):
        """
        Initialize the board by loading all vehicles from source file.
        """
        # get board length
        self.board_len = int(source_file.strip("./data/input/Rushhour").split('x')[0])

        # fill board with None
        matrix = [[None for i in range(self.board_len)] for j in range(self.board_len)]

        # for all cars in the csv file create the car and put on board
        with open(source_file, 'r') as file:
            reader = csv.reader(file)
            file.readline()

            for row in reader:
                vehicle = Car(row[0], row[1], int(row[2]) - 1, int(row[3]) - 1, int(row[4]))
                self.cars[vehicle.car_id] = vehicle

                matrix[vehicle.row][vehicle.column] = vehicle.car_id
                if vehicle.orientation == "H":
                    matrix[vehicle.row][vehicle.column + 1] = vehicle.car_id
                    if vehicle.length == 3:
                        matrix[vehicle.row][vehicle.column + 2] = vehicle.car_id
                else:
                    matrix[vehicle.row + 1][vehicle.column] = vehicle.car_id
                    if vehicle.length == 3:
                        matrix[vehicle.row  + 2][vehicle.column] = vehicle.car_id

        return matrix


    def update_matrix(self, move, car):
        """
        Move car and update the board accordingly.
        """

        # replace car spaces with None, remove car from board
        self.remove_car(car)

        # update car 
        car.move_car(move)

        # fill up the cars new spaces on board, place car back on board
        self.place_car(car)

    def remove_car(self, car):
        """
        Remove car on board from it's previous position.
        """
        self.matrix[car.row][car.column] = None
        if car.orientation == "H":
            self.matrix[car.row][car.column + 1] = None
            if car.length == 3:
                self.matrix[car.row][car.column + 2] = None
        else:
            self.matrix[car.row + 1][car.column] = None
            if car.length == 3:
                self.matrix[car.row  + 2][car.column] = None


    def place_car(self, car):
        """
        Place car on board according to it's current position.
        """
        self.matrix[car.row][car.column] = car.car_id
        if car.orientation == "H":
            self.matrix[car.row][car.column + 1] = car.car_id
            if car.length == 3:
                self.matrix[car.row][car.column + 2] = car.car_id
        else:
            self.matrix[car.row + 1][car.column] = car.car_id
            if car.length == 3:
                self.matrix[car.row  + 2][car.column] = car.car_id

    def print(self):
        """
        Print board. 
        """ 
        for row in self.matrix:
            print(row)
        print()

    def add_move(self, id, move):
        self.moves.append((id, move))

    def is_solution(self):
        """
        Check if the current configuration is a solution. 
        """
        if self.matrix[self.cars['X'].row][-1] == 'X':
            return True
        
        return False