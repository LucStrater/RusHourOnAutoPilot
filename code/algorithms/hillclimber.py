from .randomise import Randomize_Hillclimber as rd
from .breadth import Breadth_first_Hillclimber as bf

class Hillclimber:

    def __init__(self, board):
        self.board = board


    def get_random_solution(self, amount):
        """
        Selects the best solution out of amount number of random runs. Saves moves on board.
        """
        best = float('inf')

        for i in range(amount):
            new_board = self.board.copy()
            random = rd(new_board)
            random_moves = random.run()

            if len(random_moves) < best:
                self.board.moves = random_moves
                best = len(random_moves)

        
    def remove_back_forward(self):
        """
        Removes two consecutive moves if they did not alter the board.
        ----- BROKEN -----
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
        
        check_board = self.board.copy()

        for car_move in self.board.moves:
            if car_move != self.board.moves[0]:
                check_board.update_matrix(car_move[0], car_move[1])
            check_board.print()
        print(f'after trimming: {len(self.board.moves) - 1}', end='\n\n')


    def get_subset(self, size, portion, final=False):
        """
        Return subset of self.board.moves with size nr of moves.
        """
        subset = []
        start = int(portion * size)
        finish = int(start + size)

        if final:
            for car_move in self.board.moves[start:]:
                if car_move == self.board.moves[0]:
                    continue

                subset.append(car_move)
        else:
            for car_move in self.board.moves[start:finish]:
                if car_move == self.board.moves[0]:
                    continue

                subset.append(car_move)
        
        return subset

    
    def trace_moves(self, start_board, subset):
        """
        Performs the subset of moves on the inputted matrix to create the sub solution for BF_shortening
        """
        sub_solution = start_board.copy()
        sub_solution.moves = [('Car', 'Move')]

        for i in range(len(subset)):
            car_move = subset[i]
            sub_solution.update_matrix(car_move[0], car_move[1])
        
        return sub_solution
        
            
    def breadth_first_shortening(self, division):
        """
        Runs a BFS on equal length parts of the solution move set.
        """
        chunk_size = round(len(self.board.moves) / division, 0)
        start_board = self.board.copy()
        start_board.moves = [self.board.moves[0]]

        improved_moves = [self.board.moves[0]]

        print(f'start {division} BFS sets')
        for i in range(division):
            
            # 1. get subset of moves
            if i == division - 1:
                final = True
                subset = self.get_subset(chunk_size, i, final)
            else:
                subset = self.get_subset(chunk_size, i)
            
            if len(subset) == 0:
                print(f'BFS {i + 1} skipped')
                continue
            
            # 2. create sub_solution with self.trace_moves(start_board, subset)
            sub_solution = self.trace_moves(start_board, subset)

            if start_board.matrix == sub_solution.matrix:
                print(f'BFS {i + 1} skipped')
                continue
            
            # 3. do BFS from start_board to sub_solution
            breadth = bf(start_board, sub_solution)
            bf_moves = breadth.run()

            for move in bf_moves:
                improved_moves.append(move)

            print(f'{len(subset)} to {len(bf_moves)}')
            print(f'BFS {i + 1}')

            # 4. sub_solution becomes start_board
            start_board = sub_solution

        self.board.moves = improved_moves


    def run(self, random_nr, bf_division):
        """
        Run hillclimber. TODO
        """
        print(f'{random_nr} random runs')
        self.get_random_solution(random_nr)
        print(f'Finished: {len(self.board.moves) - 1} moves', end='\n\n')

        # self.remove_back_forward()

        # division = round((len(self.board.moves) - 1) / 100)

        self.breadth_first_shortening(bf_division)
        print(f'Finished: {len(self.board.moves) - 1} moves', end='\n\n')

        for i in range(len(self.board.moves) - 1):
            car_move = self.board.moves[i + 1]
            self.board.update_matrix(car_move[0], car_move[1])
        
        if self.board.is_solution():
            print('solution is valid')
        else:
            print('you fucked up')


        return self.board.moves