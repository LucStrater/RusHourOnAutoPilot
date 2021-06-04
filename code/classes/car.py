
class Car():
    
    def __init__(self, car_id, orientation, column, row, length):
        self.car_id = car_id
        self.orientation = orientation
        self.column = column
        self.row = row
        self.length = length


    def move_car(self, move):
        """
        Check car orientation and move it the given amount in that direction.
        """
        # if H then self.column new
        if self.orientation == "H":
            self.column += move

        # if V than self.row new
        elif self.orientation == "V":
            self.row += move
        

    def is_valid(self, move, board):
        """ 
        Check validity of move on the current board configuration.
        """
        if move in get_possibilities(board):
            return True

        return False


    def get_possibilities(self, board):
        """
        Return list with legal moves.
        """
        possibilities = set()

        # horizontal left
        # print(f'car {self.car_id}. orientation: {self.orientation}, column: {self.column}, row: {self.row}')
        if self.orientation == 'H' and self.column != 0:
            for i in range(1, self.column + 1):
                if board.matrix[self.row][self.column - i] == None:
                    possibilities.add(-i)
                else:
                    break

        # horizontal right
        if self.orientation == 'H' and self.column != board.board_len:
            for i in range(self.length, board.board_len - self.column):
                if board.matrix[self.row][self.column + i] == None:
                    possibilities.add(i - self.length + 1)
                else:
                    break

        # vertical up
        if self.orientation == 'V' and self.row != 0:
            for i in range(1, self.row + 1):
                if board.matrix[self.row - i][self.column] == None:
                    possibilities.add(-i)
                else:
                    break

        # vertical down
        if self.orientation == 'V' and self.row != board.board_len:
            for i in range(self.length, board.board_len - self.row):
                if board.matrix[self.row + i][self.column] == None:
                    possibilities.add(i - self.length + 1)
                else:
                    break

        # print(f'possibilities for car {self.car_id}: {possibilities}')
        
        return list(possibilities)


    def has_legal_moves(self, board):
        """
        Check if car has legal moves
        """
        if not self.get_possibilities(board): 
            return False

        return True


    def __repr__(self):
        """
        Make sure that the object is printed properly if it is in a list/dict.
        """
        return self.car_id
