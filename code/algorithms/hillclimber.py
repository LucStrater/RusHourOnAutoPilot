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


    def state_trace(self, matrix):
        """
        Perfoms all moves from move set and returns the last state that was equal to the start state.
        """
        tracer = self.board.copy()
        tracer.moves.pop(0)
        move_indices = []

        count = 1
        for move in tracer.moves:
            tracer.update_matrix(move[0], move[1])

            if tracer.matrix == matrix:
                move_indices.append(count)
            
            count += 1
        
        return move_indices


    def delete_moves(self, start, finish):
        """
        Delets all moves between and including start and finish from self.board.moves
        """
        for i in range(start, finish + 1):
            self.board.moves[i] = None
        
        filtered_moves = [move for move in self.board.moves if move != None]
        self.board.moves = filtered_moves
    
    
    def archive_tracing(self):
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
        
        if len(move_archive) == 0:
            return None

        good_moves = list(move_archive.keys())
        bad_moves = list(move_archive.values())

        best = 0
        for i in range(len(good_moves)):
            diff = bad_moves[i] - good_moves[i]
            if diff > best:
                best = diff
                index = i

        return (good_moves[index], bad_moves[index])


    def archive_2(self):
        """
        loop over moves
        voer moves uit
        check archief
            aanwezig -> mark alle moves tussen archief en nu None
                     -> return True
            niet aanwezig -> voeg toe aan archief
            return False
        """
        tracer = self.board.copy()
        tracer.moves.pop(0)
        archive = {}
        archive[str(tracer.matrix)] = 0

        for i in range(len(tracer.moves)):
            move = tracer.moves[i]
            tracer.update_matrix(move[0], move[1])

            matrix = str(tracer.matrix)

            if matrix in archive:
                start = archive[matrix]
                
                
                return True
            else:
                archive[matrix] = i + 1
        

        #     # check archief
        #     if matrix in archive:
        #         i2 = archive[matrix]

        #         # zet moves naar None
        #         for j in range(i2,i):
        #             #self.board.moves.pop(i2)
        #             self.board.moves[j] = None

        #         # verwijder None uit moves
        #         filtered_moves = [move for move in self.board.moves if move != None]
        #         self.board.moves = filtered_moves
        #         return True
        #     else:
        #         archive[matrix] = i + 1

        return False


    def test(self, good, bad):

        test_good = self.board.copy()
        for i in range(good + 1):
            car_move = test_good.moves[i + 1]
            test_good.update_matrix(car_move[0], car_move[1])
        
        test_bad = self.board.copy()
        for i in range(bad + 1):
            car_move = test_bad.moves[i + 1]
            test_bad.update_matrix(car_move[0], car_move[1])
            
        if test_good.matrix != test_bad.matrix:
            return False
        
        return True


    def run(self, random_nr, trace_itr):
        """
        Run hillclimber state trace
        """
        # RANDOM
        random_start = time.perf_counter()
        print(f'\n{random_nr} random runs')
        self.get_random_solution(random_nr)
        random_finish = time.perf_counter()
        print(f'Finished: {len(self.board.moves) - 1} moves\nRuntime: {round(random_finish - random_start, 2)}', end='\n\n')
        

        # BACK-FORWARD
        self.remove_back_forward()
        print(f'after back-forward trimming: {len(self.board.moves) - 1}', end='\n\n')

        # # START TRACE
        # print(f'before start tracing: {len(self.board.moves) - 1}')
        # traced_moves = self.state_trace(self.board.matrix)
        # if len(traced_moves) > 0:
        #     self.delete_moves(1, traced_moves[-1])
        # print(f'after start tracing: {len(self.board.moves) - 1}', end='\n\n')
        
        # # FINISH TRACE
        # print(f'before finish tracing: {len(self.board.moves) - 1}')
        # end_board = self.trace_moves(self.board, self.board.moves[1:-1])
        # traced_moves = self.state_trace(end_board)
        # print(f'after finish tracing: {len(self.board.moves) - 1}', end='\n\n')

        # ### ARCHIVE TRACE
        trace_start = time.perf_counter()
        for i in range(trace_itr):

            good_bad = self.archive_tracing()

            if good_bad == None:
                print('none found')
                break
            if not self.test(good_bad[0], good_bad[1]):
                print(f'test failed {i}')
                break

            self.delete_moves(good_bad[0] + 2, good_bad[1] + 1)
            if i % 100 == 0:
                print(f'iteration {i}', end='\n\n')

        trace_finish = time.perf_counter()
        print(f'Finished: {len(self.board.moves) - 1} moves\nRuntime: {round(trace_finish - trace_start, 2)}', end='\n\n')

        #TODO: breadth first met archive

        if not self.check_solution():
            print('Error: Moveset is not a valid solution.', end='\n\n')

        return self.board.moves