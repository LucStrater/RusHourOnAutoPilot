class Car():
    """
    The car class represents a rush hour board car and has only static data and is part of the environment.
    """
    def __init__(self, cid, orientation, length):
        self.id = cid
        self.orientation = orientation
        self.length = length

    def __repr__(self):
        """
        Make sure that the object is printed properly.
        """
        return self.cid

    def __hash__(self):
        """
        Make sure the car object is hashed according to the id (which is unique).
        """
        return self.cid