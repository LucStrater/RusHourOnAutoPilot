
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

    def get_possibilities(self, board):
        """
        Return set with legal moves.
        """
        possibilities = set()

        # horizontal left
        print(f'orientation: {self.orientation}, column: {self.column}, row: {self.row}')
        if self.orientation == 'H' and self.column != 0:
            for i in range(1, 1 + 1):
                if board[self.row][self.column - i] == None:
                    possibilities.add(-i)
                break

        # horizontal right
        elif self.orientation == 'H' and self.column != board.board_len:
            for i in range(self.length, board.board_len - self.column):
                if board[self.row][self.column + i] == None:
                    possibilities.add(i)
                break

        # vertical up
        elif self.orientation == 'V' and self.row != 0:
            for i in range(1, self.row + 1):
                if board[self.row - i][self.column] == None:
                    possibilities.add(-i)
                break

        # vertical down
        elif self.orientation == 'V' and self.row != board.board_len:
            for i in range(self.length, board.board_len - self.row):
                if board[self.row + i][self.column] == None:
                    possibilities.add(i)
                break

        
        return possibilities

    def has_legal_moves(self):
        if len(self.get_possibilities()) == 0:
            return False

        return True

    def __repr__(self):
        """
        Make sure that the object is printed properly if it is in a list/dict.
        """
        return self.car_id
