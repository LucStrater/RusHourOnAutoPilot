from .randomise import Randomize_Hillclimber as rd
from .breadth import Breadth_first_Hillclimber as bf
import time
import copy

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
        """
        for i in range(len(self.board.moves)):

            if i == len(self.board.moves) - 2:
                break
            elif self.board.moves[i + 1] == None:
                continue

            move_1 = self.board.moves[i + 1]
            move_2 = self.board.moves[i + 2]

            if move_1[0] == move_2[0] and move_1[1] == -move_2[1]:
                self.board.moves[i + 1] = None
                self.board.moves[i + 2] = None
        
        filtered_moves = [move for move in self.board.moves if move != None]
        self.board.moves = filtered_moves


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


    def check_solution(self):
        """
        Checks if the move set obtained leads to a solution.
        """
        for i in range(len(self.board.moves) - 1):
            car_move = self.board.moves[i + 1]
            self.board.update_matrix(car_move[0], car_move[1])
        
        if self.board.is_solution():
            return True
        
        return False


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

        if not self.check_solution():
            print('Error: Moveset is not a valid solution.', end='\n\n')

        return self.board.moves

#########################################################################################################################

class Hillclimber_state_trace(Hillclimber):

    # def get_random_solution(self, amount):
    #     """
    #     Selects the best solution out of amount number of random runs. Saves moves on board.
    #     """
    #     best = float('inf')
    #     count = 1

    #     while best > 40000:
    #         new_board = self.board.copy()
    #         random = rd(new_board)
    #         random_moves = random.run()
    #         print(len(random_moves))

    #         if len(random_moves) < best:
    #             self.board.moves = random_moves
    #             best = len(random_moves)
            
    #         print(f'{count}. {best}')
    #         count += 1

    
    def state_tracer(self):
        """
        Makes moves and looks for doubly visited states
        """
        tracer = self.board.copy()
        tracer.moves.pop(0)
        archive = {}
        move_archive = {}

        # loop over first 'chunk_size' moves in solution set
        for i in range(len(tracer.moves)):

            # voer move uit op tracer bord
            car_move = tracer.moves[i]
            tracer.update_matrix(car_move[0], car_move[1])

            # check of tracer matrix in archive zit
            matrix = str(tracer.matrix)
            if matrix in archive:
                # log de moves 
                arch_index = archive[matrix]
                move_archive[arch_index] = i
            else:
                # voeg tracer matrix toe aan archive
                archive[matrix] = i

        return move_archive


    def clean_up(self, move_archive):
        """
        Go through dict and delete subset of moves in order of size, starting with biggest.
        """
        while True:
            # quit when dict is empty
            if len(move_archive) == 0:
                break

            # find the biggest difference pair
            best = 0
            for key in move_archive:
                diff = move_archive[key] - key
                if diff > best:
                    best = diff
                    good_move = key
                    bad_move = move_archive[key]
            
            # check if moves don't partially fall into recently removed chunk
            if self.board.moves[good_move + 2] != None and self.board.moves[bad_move + 1] != None:
                for i in range(good_move + 2, bad_move + 2):
                    self.board.moves[i] = None
                move_archive.pop(good_move)
            else:
                move_archive.pop(good_move)
        
        # delete moves from moves list
        filtered_moves = [move for move in self.board.moves if move != None]
        self.board.moves = filtered_moves


    def bf_archive(self):
        """
        Makes moves on tracer board and returns dict with matrix as key and number of moves as value
        """
        board = self.board.copy()
        board.moves.pop(0)
        archive = {}

        arch_move_count = 0
        archive[str(board.matrix)] = arch_move_count

        for move in board.moves:
            arch_move_count += 1

            board.update_matrix(move[0], move[1])
            archive[str(board.matrix)] = arch_move_count
        
        return archive
    
    
    def bf_shortening(self, state_archive, depth):
        """
        Performs BFS up to given depth to search for shorter paths to states in archive
        """
        board = self.board.copy()
        board.moves = []
        improved_moves = []

        count = 0

        while True:
            breadth = bf(board, state_archive)
            good_moves = breadth.run(depth)
            
            if good_moves == None:
                if count % 100 == 0:
                    print('bad')

                # perform depth + 1 moves from self.board.moves on board
                start = state_archive[str(board.matrix)] + 1
                finish = depth + 2

                for move in self.board.moves[start:finish]:
                    board.update_matrix(move[0], move[1])
                    board.moves.append(move)

                    if board.is_solution():
                        break
            else:
                if count % 100 == 0:
                    print(f'good: {len(good_moves)}')

                # perform good_moves on board
                for move in good_moves:
                    board.update_matrix(move[0], move[1])
                    board.moves.append(move)
            
            if board.is_solution():
                break
            
            count += 1
            if count % 100 == 0:
                print(count)
                print(len(board.moves))

                
        board.moves.insert(0, ('Move', 'Car'))
        print(len(board.moves))
            
            


    def run(self, random_nr):
        """
        Run hillclimber state trace
        """
        ### RANDOM
        random_start = time.perf_counter()
        print(f'\n{random_nr} random runs')
        self.get_random_solution(random_nr)
        random_finish = time.perf_counter()

        print(f'Finished: {len(self.board.moves) - 1} moves\nRuntime: {round(random_finish - random_start, 2)}', end='\n\n')
        
        ### BACK-FORWARD TRIMMING
        self.remove_back_forward()
        print(f'after back-forward trimming: {len(self.board.moves) - 1}', end='\n\n')

        ### STATE TRACING
        while True:

            good_bad_dict = self.state_tracer()
            if len(good_bad_dict) == 0:
                break

            self.clean_up(good_bad_dict)

        print(f'After state tracing: {len(self.board.moves) - 1}', end='\n\n')

        # ### BREADTH FIRST SHORTENING
        # state_archive = self.bf_archive()
        # bf_depth = 3
        # self.bf_shortening(state_archive, bf_depth)


        ### FINAL CHECK
        if not self.check_solution():
            print('Error: Moveset is not a valid solution.', end='\n\n')

        return self.board.moves