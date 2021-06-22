from code.classes.model import Model
# from code.classes.board import Board
# from code.visualisation.pygame_viz import Game
# from code.algorithms import randomise, greedy
from sys import argv
# from code.algorithms import depth_first as df
# from code.algorithms import iterative_deepening as id
from code.algorithms import depth_first_v3 as df
from code.algorithms import breadth_first_v3 as bf
from code.algorithms import iterative_deepening_v3 as itd
from code.algorithms import randomise_v3 as rd
from code.algorithms import hillclimber_v3 as hc
from code.algorithms import a_star_v3 as ast
from code.algorithms import a_star_io_v3 as asio
# from code.algorithms import pruned_a_star as pas
# from code.algorithms import breadth as bf
# from code.algorithms import randomise_a_star as ras
from code.output import output
import time


def main():

    rushHourBoard = get_board()

    algorithm = get_algorithm()
    
    if algorithm == 'randomise':
        # user input number of random runs?
        moves = randomise(rushHourBoard)
    elif algorithm == 'breadth first':
        # user input maximum depth?
        moves = breadth_first(rushHourBoard)
    elif algorithm == 'depth first':
        moves = depth_first(rushHourBoard)
    elif algorithm == 'iterative deepening':
        moves = iterative_deepening(rushHourBoard)
    elif algorithm == 'a*':
        moves = a_star(rushHourBoard)
    elif algorithm == 'hill climber':
        moves = hillclimber(rushHourBoard)

    output.export_to_csv(moves, './data/output/output.csv')

def get_board():
    """
    Gets the board from the user
    """
    good_boards = ['6x6_1', '6x6_2', '6x6_3', '9x9_4', '9x9_5', '9x9_6', '12x12_7']
    good_input = False
    
    print('Welcome to RusHourOnAutoPilot!\n\nAvailable Boards:\n6x6: 1, 2, 3\n9x9: 4, 5, 6\n12x12: 7', end='\n\n')

    while not good_input:
        board = input('Type "<size>_<number>" for the board you want to solve (e.g. "6x6_1"),\n or type "new" to generate a random new board.\n')

        if board in good_boards:
            board_title = f'./data/input/Rushhour{board}.csv'
            rushHourBoard = Model(board_title)
            good_input = True
        elif board == 'new':
            pass
        else:
            continue
    
    return rushHourBoard


def get_algorithm():
    """
    Gets the algorithm from the user
    """
    good_algorithms = ['randomise', 'breadth first', 'depth first', 'iterative deepening', 'a*', 'hill climber']
    good_input = False

    print('\nAvailable algorithms:\n\nRandomise\nBreadth First\nDepth First\nIterative Deepening\nA*\nHill Climber\n')

    while not good_input:
        algorithm = input('Type the name of the algorithm you want to use: ')

        if algorithm.lower() in good_algorithms:
            return algorithm.lower()
        
        print('Error: invalid name. Please make sure the name is spelled correctly, including any spaces.', end='\n\n')


def randomise(rushHourBoard):
    """
    Solve the board using the Randomise algorithm (see randomise.py for details)
    """
    print('\nRandomise start', end='\n\n')
    start = time.perf_counter()

    randomise = rd.Randomise(rushHourBoard)
    moves = randomise.run()

    finish = time.perf_counter()
    print(f'Randomise found a solution in {len(moves) - 1} moves. See data.output.output.csv')
    print(f'Run time: {round(finish - start, 2)} seconds', end = '\n\n')

    return moves


def breadth_first(rushHourBoard):
    """
    Solve the board using the Breadth First algorithm (see breadth_first.py for details)
    """
    print('\nBreadth First start', end='\n\n')
    start = time.perf_counter()

    breadth = bf.Breadth_first(rushHourBoard)
    moves = breadth.run()

    finish = time.perf_counter()
    print(f'Breadth First found a solution in {len(moves) - 1} moves. See data.output.output.csv')
    print(f'Run time: {round(finish - start, 2)} seconds', end = '\n\n')

    return moves


def depth_first(rushHourBoard):
    """
    Solve the board using the Depth First algorithm (see depth_first.py for details)
    """
    good_input = False
    while not good_input:
        try:
            max_depth = int(input('Maximum depth: '))
            if max_depth > 0:
                good_input = True
                continue
        except ValueError:
            pass

        print('\nPlease type a positive number.\n')

    print('\nDepth First start', end='\n\n')
    start = time.perf_counter()

    depth = df.DepthFirst(rushHourBoard)
    moves = depth.run(max_depth)

    finish = time.perf_counter()
    print(f'Depth First found a solution in {len(moves) - 1} moves. See data.output.output.csv')
    print(f'Run time: {round(finish - start, 2)} seconds', end = '\n\n')

    return moves


def iterative_deepening(rushHourBoard):
    """
    Solve the board using the Iterative Deepening algorithm (see iterative_deepening.py for details)
    """
    print('\nIterative Deepening start', end='\n\n')    
    start = time.perf_counter()

    it_deep = itd.Iterative_deepening(rushHourBoard)
    moves = it_deep.run()

    finish = time.perf_counter()
    print(f'Iterative Deepening found a solution in {len(all_moves) - 1} moves. See data.output.output.csv')
    print(f'Run time: {round(finish - start, 2)} seconds', end = '\n\n')

    return moves


def a_star(rushHourBoard):
    """
    Solve the board using the A* algorithm (see a_star.py for details)
    """
    print('\nA* start', end='\n\n')  
    start = time.perf_counter()

    a_star = ast.A_star(rushHourBoard)
    moves = a_star.run()

    finish = time.perf_counter()
    print(f'A* found a solution in {len(moves) - 1} moves. See data.output.output.csv')
    print(f'runtime: {round(finish - start, 2)} seconds', end = '\n\n')

    return moves


def hillclimber(rushHourBoard):
    """
    Solve the board using the Hill Climber algorithm (see hill_climber.py for details)
    """
    good_input = False
    while not good_input:
        try:
            random_nr = int(input('Number of random runs: '))
            max_score = int(input('Maximum allowed heuristic score: '))
            low_max_score = int(input('Maximum allowed heuristic score after failed A* search: '))

            if random_nr > 0 and max_score > 0 and low_max_score > 0:
                good_input = True
                continue
        except ValueError:
            pass
        
        print('\nPlease type positive numbers.\n')

    ### dit ook inputten?
    max_val = 6000
    max_plus = 8
    low_max_plus = 1
    max_val_plus = 1200

    print('\nHill climber start', end='\n\n') 
    start = time.perf_counter()

    hillclimber = hc.Hillclimber(rushHourBoard)
    moves = hillclimber.run(random_nr, max_score, max_plus, low_max_score, low_max_plus, max_val, max_val_plus)

    finish = time.perf_counter()
    print(f'Hillclimber found solution in {len(moves) - 1} moves. See data.output.output.csv')
    print(f'runtime: {round(finish - start, 2)} seconds', end = '\n\n')

    return moves


if __name__ == "__main__":
    main()
#=====================================================================================================================#
# def main():
    # # get board title from the terminal
    # if len(argv) not in [1, 2, 3]:
    #     print("Usage: python3 main.py [filename (example: <6x6_1>)]")
    #     exit(1)

    # if len(argv) == 2:
    #     board_title = f"./data/input/Rushhour{argv[1]}.csv"
    # else:
    #     board_title = './data/input/Rushhour6x6_1.csv'

    # # init the board
    # rushHourBoard = Model(board_title)

    # ########################### Randomise ###########################
    # start = time.perf_counter()

    # randomise = rd.Randomise(rushHourBoard)
    # all_moves = randomise.run()
    # print(f"best solution for randomise: {all_moves}. This takes {len(all_moves) - 1} moves.")

    # # output.export_to_csv(all_moves, './data/output/output.csv')

    # finish = time.perf_counter()
    # print(f'runtime randomise: {round(finish - start, 2)} seconds')
    # print()

    # ############################# Random ################################

    # # # solve the board using random moves and print first 10 moves
    # # all_moves = randomise.run_milestone1(rushHourBoard, True)[0]

    # # # save moves to output file
    # # output.export_to_csv(all_moves, './data/output/output.csv')

    # # average amount of steps for 100 iterations of randomise to solve the board
    # counters = 0
    # maximum = 0
    # minimum = float('inf')

    # for i in range(100):
    #     rushHourBoard = Board(board_title)
    #     counter = randomise.run_milestone1(rushHourBoard, False)[1]
    #     if counter < minimum:
    #         minimum = counter
    #     if counter > maximum:
    #         maximum = counter

    #     counters += counter

    # print("[Baseline: make random moves until solved]")
    # print(f"The average amount of steps of 100 iterations is: {counters/100}")
    # print(f"The maximum steps of 100 iterations is: {maximum}")
    # print(f"The minimum steps of 100 iterations is: {minimum}")
    # print()

    # ####################### Greedy ####################################

    # # average amount of steps for 100 iterations of greedy 1 to solve the board
    # counters_greedy_1 = 0
    # maximum_greedy_1 = 0
    # minimum_greedy_1 = float('inf')
    # for i in range(100):
    #     rushHourBoard = Board(board_title)
    #     counter_greedy_1 = greedy.run_1(rushHourBoard)
    #     if counter_greedy_1 < maximum_greedy_1:
    #         minimum_greedy_1 = counter_greedy_1
    #     if counter_greedy_1 > maximum_greedy_1:
    #         maximum_greedy_1 = counter_greedy_1

    #     counters_greedy_1 += counter_greedy_1

    # print("[Greedy 1: if row of car X is empty -> finish]")
    # print(f"The average amount of steps of 100 iterations is: {counters_greedy_1/100}")
    # print(f"The maximum steps of 100 iterations is: {maximum_greedy_1}")
    # print(f"The minimum steps of 100 iterations is: {minimum_greedy_1}")
    # print(f"That is {round(- (counters_greedy_1/counters - 1) * 100)}% better than the baseline")
    # print()

    # # average amount of steps for 100 iterations of greedy 2 to solve the board
    # counters_greedy_2 = 0
    # maximum_greedy_2 = 0
    # minimum_greedy_2 = float('inf')
    # for i in range(100):
    #     rushHourBoard = Board(board_title)
    #     counter_greedy_2 = greedy.run_2(rushHourBoard)
    #     if counter_greedy_2 < maximum_greedy_2:
    #         minimum_greedy_2 = counter_greedy_2
    #     if counter_greedy_2 > maximum_greedy_2:
    #         maximum_greedy_2 = counter_greedy_2

    #     counters_greedy_2 += counter_greedy_2

    # print("[Greedy 2: if cars on row of car X can all be moved -> move them + Greedy 1]")
    # print(f"The average amount of steps of 100 iterations is: {counters_greedy_2/100}")
    # print(f"The maximum steps of 100 iterations is: {maximum_greedy_2}")
    # print(f"The minimum steps of 100 iterations is: {minimum_greedy_2}")
    # print(f"That is {round(- (counters_greedy_2/counters - 1) * 100)}% better than the baseline")
    # print()

    # # average amount of steps for 100 iterations of greedy 3 to solve the board
    # counters_greedy_3 = 0
    # maximum_greedy_3 = 0
    # minimum_greedy_3 = float('inf')
    # for i in range(100):
    #     rushHourBoard = Board(board_title)
    #     counter_greedy_3 = greedy.run_3(rushHourBoard)
    #     if counter_greedy_3 < minimum_greedy_3:
    #         minimum_greedy_3 = counter_greedy_3
    #     if counter_greedy_3 > maximum_greedy_3:
    #         maximum_greedy_3 = counter_greedy_3

    #     counters_greedy_3 += counter_greedy_3

    # print("[Greedy 3: if Greedy 1 & 2 not possible, try randomly move a car that blocks road for car X]")
    # print(f"The average amount of steps of 100 iterations is: {counters_greedy_3/100}")
    # print(f"The maximum steps of 100 iterations is: {maximum_greedy_3}")
    # print(f"The minimum steps of 100 iterations is: {minimum_greedy_3}")
    # print(f"That is {round(- (counters_greedy_3/counters - 1) * 100)}% better than the baseline")
    # print()

    #     ########################### Depth first ###########################
    # start = time.perf_counter()

    # depth = df.DepthFirst(rushHourBoard)
    # all_moves = depth.run()
    # print(f"best solution for depth first: {all_moves}. This takes {len(all_moves) - 1} moves.")

    # # output.export_to_csv(all_moves, './data/output/output.csv')

    # finish = time.perf_counter()
    # print(f'runtime depth first: {round(finish - start, 2)} seconds')
    # print()

    ########################### A* #############################

    # start = time.perf_counter()

    # a_star = ast.A_star(rushHourBoard)
    # moves = a_star.run()
    # print(f"best solution for A*: {moves}. This takes {len(moves) - 1} moves.")

    # finish = time.perf_counter()
    # print(f'runtime: {round(finish - start, 2)} seconds')
    # print()

    #   ########################### A* IO #############################
    # state.print()
    # board = Model(board_title)

    # start = time.perf_counter()

    # a_star_io = asio.A_star(board, state)
    # moves = a_star_io.run()
    # print(f"best solution for A*: {moves}. This takes {len(moves) - 1} moves.")

    # finish = time.perf_counter()
    # print(f'runtime: {round(finish - start, 2)} seconds')
    # print()

    # ########################### PRUNED A* ##############################

    # # init the board
    # rushHourBoard = Board(board_title)

    # start = time.perf_counter()

    # pruned_a_star = pas.Pruned_a_star(rushHourBoard)
    # moves = pruned_a_star.run()
    # print(f"best solution for A*: {moves}. This takes {len(moves) - 1} moves.")

    # finish = time.perf_counter()
    # print(f'runtime: {round(finish - start, 2)} seconds')
    # print()



    # ######################## Iterative deepening #####################

    # start = time.perf_counter()

    # depth = id.Iterative_deepening(rushHourBoard)
    # all_moves = depth.run()
    # print(f"best solution for iterative deepening: {all_moves}. This takes {len(all_moves) - 1} moves.")

    # # output.export_to_csv(all_moves, './data/output/output.csv')

    # finish = time.perf_counter()
    # print(f'runtime iterative deepening: {round(finish - start, 2)} seconds')
    # print()

    ######################## Breadth First #####################

    # bf_start = time.perf_counter()

    # breadth_first = bf.Breadth_first(rushHourBoard)
    # bf_moves = breadth_first.run()
    # print(f'Breadth First found a solution in {len(bf_moves) - 1} moves.')

    # bf_finish = time.perf_counter()
    
    # print(f'runtime V2: {round(bf_finish - bf_start, 2)} seconds', end = '\n\n')
    # print()

    # ######################## Hillclimber #####################
    # hc_random_nr = 20

    # hc_start = time.perf_counter()

    # max_score = 25
    # low_max_score = 9
    # max_val = 6000
    # max_plus = 8
    # low_max_plus = 1
    # max_val_plus = 1200
    # hillclimber = hc.Hillclimber(rushHourBoard)
    # hc_moves = hillclimber.run(hc_random_nr, max_score, max_plus, low_max_score, low_max_plus, max_val, max_val_plus)
    # print(f'Hillclimber found solution in {len(hc_moves) - 1} moves.')

    # hc_finish = time.perf_counter()
    
    # print(f'runtime: {round(hc_finish - hc_start, 2)} seconds', end = '\n\n')
    # print(f'max_score = {max_score} low_max_score = {low_max_score} max_val = {max_val} max_plus = {max_plus} low_max_plus = {low_max_plus} max_val_plus = {max_val_plus}')

    # output.export_to_csv(hc_moves, './data/output/output.csv')

    ######################## Visualisation #####################

    # vizBoard = Model(board_title)
    # vizBoard.moves = hc_moves[1:]
    
    # viz = Game(vizBoard)
    # viz.run()


