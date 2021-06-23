from .randomise import Randomise as rd
import time
import copy
from code.algorithms import a_star_io as asio

class Hillclimber:
    """
    A hill climbing approach to solving a rush hour game.
    It aims to obtain and improve a solution in the following steps:
    1.  RANDOM: It obtains the best solution out of an inputted amount of random runs.
    2.  BACK-FORWARD TRIMMING: It takes out all moves where a car was moved back and forward consecutively.
    3.  STATE TRACING: It checks the solution path for doubly visited states and deletes moves between the first and second visit.
    4.  A* SHORTENING:
      4a.  It compares different states in the solution path using a heuristic to find boards that look alike.
           The maximum allowed heuristic score is inputted by the user.
      4b.  It runs an A* algorithm to find a shorter path between boards that look alike.
           To limit computation time, the maximum number of states an A* searches is inputted by the user
    5.  CLEAN FINISH: It checks the solution path to see if the finishing move could have been made sooner.
    Steps 1, 2, 3 and 4 each run until no improvement has been found.
    """

    def __init__(self, model):
        self.model = model
        self.cars = self.model.get_cars()


#================================================ Step 1. ================================================#
    def get_random_solution(self, amount):
        """
        Selects the best solution out of inputted number of random runs. Saves moves on board.
        """
        best = float('inf')

        for i in range(amount):
            new_model = self.model.copy()
            random = rd(new_model)
            random_moves = random.run()

            if len(random_moves) < best:
                self.model.moves = random_moves
                best = len(random_moves)


#================================================ Step 2. ================================================#       
    def remove_back_forward(self):
        """
        Removes two consecutive moves if they move a car back and forward.
        """
        # move set without the header strings
        moves = self.model.moves[1:]

        for i in range(len(moves)):

            if i == len(moves) - 1:
                break
            elif moves[i] == None:
                continue

            move_1 = moves[i]
            move_2 = moves[i + 1]

            # if the cars are equal and the moves are opposite
            if move_1[0] == move_2[0] and move_1[1] == -move_2[1]:
                moves[i] = None
                moves[i + 1] = None
        
        filtered_moves = [move for move in moves if move != None]
        self.model.moves[1:] = filtered_moves


#================================================ Step 3. ================================================# 
    def state_tracer(self):
        """
        Makes moves on a tracer (copied) board and looks for doubly visited states.
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

            matrix = tracer.get_tuple()

            # if doubly visited state was found
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
        Go through dict and delete subsets of moves in order of size, starting with biggest.
        """
        # move set without the header strings
        moves = self.model.moves[1:]

        while len(move_archive) != 0:

            # find the key-value pair with biggest difference
            best = 0
            for key in move_archive:
                diff = move_archive[key] - key
                if diff > best:
                    best = diff
                    good_move = key
                    bad_move = move_archive[key]
            
            # check if moves don't partially fall into recently removed chunk
            if moves[good_move + 1] != None and moves[bad_move] != None:
                for i in range(good_move + 1, bad_move + 1):
                    moves[i] = None
                move_archive.pop(good_move)
            else:
                move_archive.pop(good_move)
        
        # delete moves from moves list
        filtered_moves = [move for move in moves if move != None]
        self.model.moves[1:] = filtered_moves


#================================================ Step 4. ================================================# 
    def make_archive(self):
        """
        Makes all moves on tracer board and returns dict with matrix tuple as key and number of moves as value.
        """
        # copied model with move set without the header strings
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
            

    def heuristic(self, model, goal_model):
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
        Compares all boards on the solution path to a start board, starting at the end of the paths.
        Returns the first board with a score lesser or equal to the inputted maximum.
        """
        tracer = start_board.copy()
        tracer.moves = [('car', 'move')]
        old_position = state_archive[tracer.get_tuple()] + 1

        # make all moves to get tracer to solution state
        for move in self.model.moves[old_position:]:
            car = start_board.board.cars[move[0]]
            tracer.update_matrix(car, move[1])
            tracer.add_move(car.cid, move[1])

        # check solution state
        score = self.heuristic(start_board, tracer)
        if score <= max_score:
            return tracer

        counter = 0
        for i in reversed(range(len(tracer.moves))):
            # make moves back from solution state
            counter += 1
            move = tracer.moves[i]
            tracer.update_matrix(tracer.board.cars[move[0]], move[1] * -1)
            
            score = self.heuristic(start_board, tracer)
            if score <= max_score:
                # delete moves between tracers current config and solution state
                new_moves = tracer.moves[:len(tracer.moves) - counter]
                tracer.moves = new_moves
                break

        return tracer


    def run_a_star(self, max_score, low_max_score, max_val):
        """
        Iterates over all states in the solution path. Finds a good goal and runs A* algorithm between the start and goal.
        When a shorter path was found, the goal becomes the start for the next iteration. 
        """
        start_board = self.model.copy()
        start_board.moves = [('car', 'move')]
        state_archive = self.make_archive()

        count = 0
        input_max_score = max_score
        
        while not start_board.is_solution():
            count += 1
            # get the best goal state
            goal_model = self.find_good_goal(start_board, max_score, state_archive)

            # run A* from start to goal
            a_star_io = asio.A_star(start_board, goal_model)
            state_found, a_star_board = a_star_io.run(max_val)

            # no solution was found
            if not state_found:

                # adjust max allowed heuristic score for next iteration
                max_score = low_max_score

                # move the board one step along the solution path
                old_position = state_archive[start_board.get_tuple()] + 1
                move = self.model.moves[old_position]
                car = self.model.board.cars[move[0]]
                start_board.update_matrix(car, move[1])
                start_board.add_move(car.cid, move[1])
                continue
            
            # reset max allowed heuristic score after A* found a path
            max_score = input_max_score
            
            start_board = a_star_board
        
        self.model.moves = a_star_board.moves


#================================================ Step 5. ================================================# 
    def clean_finish(self):
        """
        Makes all moves from the solution on a tracer board and checks if the winning move can be made befor each move.
        """
        tracer = self.model.copy()
        tracer.moves = [('car','move')]
        count = 1
        red_car = self.model.board.cars['X']
        win_col = self.model.board.board_len - 1

        while not tracer.is_solution():

            for move in tracer.get_possibilities(red_car):
                red_car_col = tracer.get_car_pos(red_car)[1]
                
                # if winning move can be made
                if red_car_col + move == win_col:
                    tracer.update_matrix(red_car, move)
                    tracer.add_move(red_car.cid, move)
                    continue
            
            # perform next move in path
            given_move = self.model.moves[count]
            car = tracer.board.cars[given_move[0]]
            tracer.update_matrix(car, given_move[1])
            tracer.add_move(car.cid, given_move[1])
            count += 1
        
        self.model.moves = tracer.moves


#============================================== FINAL CHECK ==============================================# 
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


#================================================== RUN ==================================================#
    def run(self, random_nr, max_score, max_plus, low_max_score, max_val, max_val_plus):
        """
        Runs hillclimber with inputted variables.
        """
        ### 1. RANDOM
        random_start = time.perf_counter()
        print(f'\n{random_nr} random runs')
        self.get_random_solution(random_nr)
        random_finish = time.perf_counter()

        print(f'Finished: {len(self.model.moves) - 1} moves\nRuntime: {round(random_finish - random_start, 2)}', end='\n\n')
        
        ### 2. BACK-FORWARD TRIMMING
        improving = True
        while improving:
            start_len = len(self.model.moves)
            self.remove_back_forward()
            new_len = len(self.model.moves)

            if new_len == start_len:
                improving = False
                continue
            
        print(f'after back-forward trimming: {len(self.model.moves) - 1}', end='\n\n')

        ### 3. STATE TRACING
        count = 0

        improving = True
        while improving:
            good_bad_dict = self.state_tracer()

            if len(good_bad_dict) == 0:
                improving = False
                continue

            self.clean_up(good_bad_dict)

        print(f'After state tracing: {len(self.model.moves) - 1}', end='\n\n')

        ### 4. A* SHORTENING
        start = time.perf_counter()

        count = 1
        improving = True
        while improving:
            start_len = len(self.model.moves)
            self.run_a_star(max_score, low_max_score, max_val)
            finish_len = len(self.model.moves)

            max_score += max_plus
            max_val += max_val_plus

            if finish_len == start_len:
                improving = False
                continue

            print(f'A* iteration {count}: {len(self.model.moves) - 1}')
            count += 1

        finish = time.perf_counter()
        print(f'Runtime A*: {round(finish - start, 2)}', end='\n\n')
    
        ### 5. CLEAN FINISH
        self.clean_finish()

        ### FINAL CHECK
        if not self.check_solution():
            print('Error: Moveset is not a valid solution.', end='\n\n')

        return self.model.moves
