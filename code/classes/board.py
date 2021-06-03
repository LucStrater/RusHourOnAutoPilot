import csv
from .car import Car

class Board():
    def __init__(self, source_file):
        self.board_len = 0
        self.cars = {}
        self.matrix = self.load_matrix(source_file)
        

    def load_matrix(self, source_file):
        """
        Load all vehicles into the board.
        """

        # get board length
        self.board_len = int(source_file.strip("./data/Rushhour").split('x')[0])

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

        
    def print(self): 
        for row in self.matrix:
            print(row)

        for car in self.cars:
            print(car)


    def is_solution(self):
        """
        Check if the current configuration is a solution. 
        """
        pass