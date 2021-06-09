import csv
from .car import Car

class Board():

    def __init__(self, source_file):
        self.board_len = 0
        self.cars = {}
        self.matrix = self.load_matrix(source_file)

        # for BFS
        self.moves = [['car','move']]
        self.id = None
        self.depth = 0
        

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
        # update car 
        car.move_car(move)

        # replace car spaces with None, remove car from board
        for i in range(self.board_len):
            for j in range(self.board_len):
                if self.matrix[i][j] == car.car_id:
                    self.matrix[i][j] = None

        # fill up the cars new spaces on board, place car back on board
        self.place_car(car)

    
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


    def is_solution(self):
        """
        Check if the current configuration is a solution. 
        """
        if self.matrix[self.cars['X'].row][self.board_len - 1] == 'X':
            return True
        
        return False