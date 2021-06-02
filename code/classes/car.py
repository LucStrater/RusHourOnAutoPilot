
class Car():

    def __init__(self, car_id, orientation, column, row, length):
        self.car_id = car_id
        self.orientation = orientation
        self.column = column
        self.row = row
        self.length = length

    def load_car(self):
        pass

    def move_car(self):
        pass

    def is_valid(self):
        pass

    def get_possibilities(self):
        pass

    def __repr__(self):
        """
        Make sure that the object is printed properly if it is in a list/dict.
        """
        return self.car_id
