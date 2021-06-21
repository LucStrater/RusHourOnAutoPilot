from .randomise_v3 import Randomise as rd
from .breadth_first_v3 import Breadth_first_hillclimber as bf
import time
import copy

class Hillclimber:

    def __init__(self, model):
        self.model = model


    def get_random_solution(self, amount):
        """
        Selects the best solution out of amount number of random runs. Saves moves on board.
        """
        best = float('inf')

        for i in range(amount):
            new_model = self.model.copy()
            random = rd(new_model)
            random_moves = random.run()

            if len(random_moves) < best:
                self.model.moves = random_moves
                best = len(random_moves)

        
    def remove_back_forward(self):
        """
        Removes two consecutive moves if they did not alter the board.
        """
        for i in range(len(self.model.moves)):

            if i == len(self.model.moves) - 2:
                break
            elif self.model.moves[i + 1] == None:
                continue

            move_1 = self.model.moves[i + 1]
            move_2 = self.model.moves[i + 2]

            if move_1[0] == move_2[0] and move_1[1] == -move_2[1]:
                self.model.moves[i + 1] = None
                self.model.moves[i + 2] = None
        
        filtered_moves = [move for move in self.model.moves if move != None]
        self.model.moves = filtered_moves


    def state_tracer(self):
        """
        Makes moves and looks for doubly visited states
        """
        tracer = self.model.copy()
        tracer.moves.pop(0)
        archive = {}
        move_archive = {}

        for i in range(len(tracer.moves)):

            # execute move on tracer model
            car_move = tracer.moves[i]
            car = tracer.board.cars[car_move[0]]
            tracer.update_matrix(car, car_move[1])

            # check archive for tracer matrix
            matrix = tracer.get_tuple()
            if matrix in archive:
                # log the moves in move archive
                arch_index = archive[matrix]
                move_archive[arch_index] = i
            else:
                # add tracer matrix to archive
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
            if self.model.moves[good_move + 2] != None and self.model.moves[bad_move + 1] != None:
                for i in range(good_move + 2, bad_move + 2):
                    self.model.moves[i] = None
                move_archive.pop(good_move)
            else:
                move_archive.pop(good_move)
        
        # delete moves from moves list
        filtered_moves = [move for move in self.model.moves if move != None]
        self.model.moves = filtered_moves


    def bf_archive(self):
        """
        Makes moves on tracer board and returns dict with matrix as key and number of moves as value
        """
        model = self.model.copy()
        model.moves.pop(0)
        archive = {}

        arch_move_count = 0
        start_matrix = model.get_tuple()
        archive[start_matrix] = arch_move_count

        for car_move in model.moves:
            arch_move_count += 1
            car = model.board.cars[car_move[0]]

            model.update_matrix(car, car_move[1])
            matrix = model.get_tuple()
            archive[matrix] = arch_move_count
        
        return archive
    

    def bf_shortening(self, state_archive, depth):
        """
        Performs BFS up to given depth to search for shorter paths to states in archive
        """
        model = self.model.copy()
        model.moves = []
        count = 0

        while True:
            # perform BFS on model
            breadth = bf(model, state_archive)
            good_moves = breadth.run(depth)
            
            # if no better path was found
            if good_moves == None:
                # perform moves from the known path
                start = state_archive[model.get_tuple()] + 1
                finish = start + depth + 2

                for move in self.model.moves[start:finish]:
                    car = model.board.cars[move[0]]
                    model.update_matrix(car, move[1])
                    model.moves.append(move)

                    if model.is_solution():
                        break
            # if a better path was found            
            else:
                # perform good moves on board
                for move in good_moves:
                    car = model.board.cars[move[0]]
                    model.update_matrix(car, move[1])
                    model.moves.append(move)

            if model.is_solution():
                break
            
            count += 1
            if count % 1000 == 0:
                print(f'bf {count}')
                print(len(model.moves))

        # point the overarching model to the new move set
        model.moves.insert(0, ('Move', 'Car'))
        self.model.moves = model.moves
            
 
    def check_solution(self):
        """
        Checks if the move set obtained leads to a solution.
        """
        for i in range(len(self.model.moves) - 1):
            car_move = self.model.moves[i + 1]
            car = self.model.board.cars[car_move[0]]
            move = car_move[1]
            self.model.update_matrix(car, move)
        
        if self.model.is_solution():
            return True
        
        return False

    def run(self, random_nr):
        """
        Run hillclimber state trace
        """
        ### RANDOM
        random_start = time.perf_counter()
        print(f'\n{random_nr} random runs')
        self.get_random_solution(random_nr)
        random_finish = time.perf_counter()

        print(f'Finished: {len(self.model.moves) - 1} moves\nRuntime: {round(random_finish - random_start, 2)}', end='\n\n')

        ### BACK-FORWARD TRIMMING
        while True:
            start_len = len(self.model.moves)
            self.remove_back_forward()
            new_len = len(self.model.moves)

            if new_len == start_len:
                break

        finish = time.perf_counter()
        print(f'after back-forward trimming: {len(self.model.moves) - 1}\nRuntime: {round(finish - random_start, 2)}', end='\n\n')

        ### STATE TRACING
        count = 0
        while True:
            good_bad_dict = self.state_tracer()
            if len(good_bad_dict) == 0:
                break

            self.clean_up(good_bad_dict)
        
        finish = time.perf_counter()
        print(f'After state tracing: {len(self.model.moves) - 1}\nRuntime: {round(finish - random_start, 2)}', end='\n\n')

        ### BREADTH FIRST SHORTENING
        state_archive = self.bf_archive()
        bf_depth = 2
        self.bf_shortening(state_archive, bf_depth)

        ### FINAL CHECK
        if not self.check_solution():
            print('Error: Moveset is not a valid solution.', end='\n\n')

        return self.model.moves
