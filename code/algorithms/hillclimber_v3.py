from .randomise_v3 import Randomise as rd
from .breadth_first_v3 import Breadth_first_hillclimber as bf
import time
import copy
from code.algorithms import a_star_io_v3 as asio

class Hillclimber:

    def __init__(self, model):
        self.model = model
        self.cars = self.model.get_cars()


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
            if count % 20 == 0:
                print(f'bf {count}')
                print(len(model.moves))
                print()

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


    def clean_finish(self):
        """

        """
        tracer = self.model.copy()
        tracer.moves = [('car','move')]
        count = 1
        red_car = self.model.board.cars['X']
        win_col = self.model.board.board_len - 1

        while not tracer.is_solution():
            possibilities = tracer.get_possibilities(red_car)

            for move in possibilities:
                red_car_col = tracer.get_car_pos(red_car)[1]
                
                if red_car_col + move == win_col:
                    tracer.update_matrix(red_car, move)
                    tracer.add_move(red_car.cid, move)
                    continue
            
            given_move = self.model.moves[count]
            car = tracer.board.cars[given_move[0]]
            tracer.update_matrix(car, given_move[1])
            tracer.add_move(car.cid, given_move[1])
            count += 1
        
        self.model.moves = tracer.moves
            

    def heuristic(self, model, goal_model):
        """   
        Distance to goal: with a given solution from a random algorithm determine the distance of every car to its final position
        """ 
        score = 0

        for car in self.cars:
            row_model, column_model = model.get_car_pos(car)
            row_goal, column_goal = goal_model.get_car_pos(car)
            score += abs(row_model - row_goal) + abs(column_model - column_goal)

        return score


    def heuristic_2(self, model, goal_model):
        """   
        Distance to goal: with a given solution from a random algorithm determine the distance of every car to its final position
        """ 
        score = 0

        for car in self.cars:
            row_model, column_model = model.get_car_pos(car)
            row_goal, column_goal = goal_model.get_car_pos(car)
            if abs(row_model - row_goal) > 0 or abs(column_model - column_goal) > 0: 
                score += 1

        return score


    def find_good_goal(self, start_board, max_score, state_archive):
        """
        Finds the furthest removed state with the maximum heuristic score.
        """
        tracer = start_board.copy()
        tracer.moves = [('car', 'move')]
        old_position = state_archive[tracer.get_tuple()] + 1

        # make all moves to get tracer to solution state
        for move in self.model.moves[old_position:]:
            car = start_board.board.cars[move[0]]
            tracer.update_matrix(car, move[1])
            tracer.add_move(car.cid, move[1])

        # Make moves back from solution state to find the 
        # furthest removed state with acceptable heuristic score
        counter = 0
        #hier ook het eind bord meenemen!
        score = self.heuristic_2(start_board, tracer)
        if score <= max_score:
            new_moves = tracer.moves[:len(tracer.moves) - counter]
            tracer.moves = new_moves
            return tracer

        for i in reversed(range(len(tracer.moves))):
            counter += 1
            move = tracer.moves[i]
            tracer.update_matrix(tracer.board.cars[move[0]], move[1] * -1)
            
            score = self.heuristic_2(start_board, tracer)
            if score <= max_score:
                # print('max found')
                # print(counter)
                new_moves = tracer.moves[:len(tracer.moves) - counter]
                tracer.moves = new_moves
                break

        # print(f'goal - {state_archive[tracer.get_tuple()]}')
        return tracer


    def run_a_star(self, max_score, max_plus, low_max_score, low_max_plus, max_val, max_val_plus):
        """

        """
        start_board = self.model.copy()
        start_board.moves = [('car', 'move')]
        state_archive = self.bf_archive()

        max_score = 20
        count = 0
        
        
        while True:
            # if count % 5 == 0:
            #     print(f'--- {count} A* ---')
            count += 1
            # get the best goal state
            goal_model = self.find_good_goal(start_board, max_score, state_archive)
            # start_board.print()
            # goal_model.print()
            # input()

            # run A* from start to goal
            a_star_io = asio.A_star(start_board, goal_model)
            a_star_board = a_star_io.run_hillclimber(max_val)

            # no solution was found
            if a_star_board == None:
                # print('None found')

                # adjust max allowed heuristic score
                max_score = low_max_score

                # move the board one step along the established path
                old_position = state_archive[start_board.get_tuple()] + 1
                move = self.model.moves[old_position]
                car = self.model.board.cars[move[0]]
                start_board.update_matrix(car, move[1])
                start_board.add_move(car.cid, move[1])
                continue
            
            # reset max allowed heuristic score after A* found
            max_score = 20
            # print(len(a_star_board.moves))
            
            # stop when solution has been found
            if a_star_board.is_solution():
                break
            
            start_board = a_star_board
        
        self.model.moves = a_star_board.moves


    def run(self, random_nr, max_score, max_plus, low_max_score, low_max_plus, max_val, max_val_plus):
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
            
        print(f'after back-forward trimming: {len(self.model.moves) - 1}', end='\n\n')

        ### STATE TRACING
        count = 0
        while True:
            good_bad_dict = self.state_tracer()
            if len(good_bad_dict) == 0:
                break

            self.clean_up(good_bad_dict)

        print(f'After state tracing: {len(self.model.moves) - 1}', end='\n\n')

        ### A*
        start = time.perf_counter()


        count = 1
        while True:
            start_len = len(self.model.moves)
            self.run_a_star(max_score, max_plus, low_max_score, low_max_plus, max_val, max_val_plus)
            finish_len = len(self.model.moves)
            max_score += max_plus
            max_val += max_val_plus


            if finish_len == start_len:
                break

            print(f'A* iteration {count}: {len(self.model.moves) - 1}')
            count += 1

        finish = time.perf_counter()
        print(f'Runtime A*: {round(finish - start, 2)}', end='\n\n')
    
        ### CLEAN FINISH
        self.clean_finish()

        ### FINAL CHECK
        if not self.check_solution():
            print('Error: Moveset is not a valid solution.', end='\n\n')

        return self.model.moves
