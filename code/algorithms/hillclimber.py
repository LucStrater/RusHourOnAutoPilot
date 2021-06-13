from .randomise import Randomize_Hillclimber as rd
from .breadth import Breadth_first_Hillclimber as bf

class Hillclimber:

    def __init__(self, board):
        self.board = board


    def get_random_solution(self, amount):
        """
        Selects the best solution out of amount number of random runs. Saves moves on board.
        """
        print(f'{amount} random runs')
        best = float('inf')

        for i in range(10):
            new_board = self.board.copy()
            random = rd(new_board)
            random_moves = random.run()

            if len(random_moves) < best:
                self.board.moves = random_moves
                best = len(random_moves)

        print(f'finished', end='\n\n')

    
    def remove_back_forward(self):
        """
        Removes two consecutive moves if they did not alter the board.
        """
        print(f'before trimming: {len(self.board.moves) - 1}')

        initial_len = len(self.board.moves)

        for i in range(initial_len):
            if i == len(self.board.moves) - 2:
                break

            move_1 = self.board.moves[i + 1]
            move_2 = self.board.moves[i + 2]

            if move_1[0] == move_2[0] and move_1[1] == -move_2[1]:
                del self.board.moves[i + 1]
                del self.board.moves[i + 2]
        
        print(f'after trimming: {len(self.board.moves) - 1}', end='\n\n')

    #TODO
    def trace_moves(self, ):
        """
        Performs the subset of moves on the inputted matrix to create the sub solution for BF_shortening
        """
        pass
        
            
    def breadth_first_shortening(self, division):
        """
        Runs a BFS on equal length parts of the solution move set.
        """
        chunk_size = round(len(self.board.moves) / division, 0)

        print(f'start: {len(self.board.moves)}')

        for i in range(division):
            print(round(i * chunk_size, 0))
        
        print(round(division * chunk_size, 0))


    def run(self):
        """
        Run hillclimber. TODO
        """
        self.get_random_solution(10)

        self.remove_back_forward()

        self.breadth_first_shortening(7)

        return self.board.moves