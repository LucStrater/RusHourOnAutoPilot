class Car():
    """
    The car class represents a rush hour board car and has only static data and is part of the environment.
    """
    def __init__(self, cid, orientation, length, const_pos):
        self.cid = cid
        self.orientation = orientation
        self.length = length
        self.const_pos = const_pos

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