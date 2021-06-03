# see line 31 and 45 onwards

class Board():
    
    def __init__(self, source_file):
        self.board_len = 0
        self.cars = {}
        self.autos = []
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
                self.autos.append(vehicle)

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

    def get_options_all_cars(self):
        for auto in self.autos:
            print(f'some car: {auto}, orientation: {auto.orientation} row: {auto.row} col: {auto.column} len: {auto.length}')

            possibilities = set()

            if auto.orientation == 'H' and auto.column != 0:
                for i in range(1, auto.column + 1):
                    if self.matrix[auto.row][auto.column - i] == None:
                        possibilities.add(-i)
                    else:
                        break

            # horizontal right
            elif auto.orientation == 'H' and auto.column != self.board_len:
                for i in range(auto.length, self.board_len - auto.column):
                    if self.matrix[auto.row][auto.column + i] == None:
                        possibilities.add(i)
                    else:
                        break

            # vertical up
            elif auto.orientation == 'V' and auto.row != 0:
                for i in range(1, auto.row + 1):
                    if self.matrix[auto.row - i][auto.column] == None:
                        possibilities.add(-i)
                    else:
                        break
                        
            # vertical down
            elif auto.orientation == 'V' and auto.row != self.board_len:
                for i in range(auto.length, self.board_len - auto.row):
                    if self.matrix[auto.row + i][auto.column] == None:
                        possibilities.add(i)
                    else:
                        break

            print(f'possibilities for car {auto}: {possibilities}')