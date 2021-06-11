class Car_BF2():

    def __init__(self, car_id, orientation, length):
        self.id = car_id
        self.orientation = orientation
        self.length = length
    
    def __repr__(self):
        """
        Make sure that the object is printed properly if it is in a list/dict.
        """
        return self.id