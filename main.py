from code.classes.model import Model
from code.classes.generate import Generate
from code.output.pygame_viz import Visualizer
from code.algorithms import depth_first as df
from code.algorithms import breadth_first as bf
from code.algorithms import iterative_deepening as itd
from code.algorithms import randomise as rd
from code.algorithms import hillclimber as hc
from code.algorithms import a_star as ast
from code.output import output
import time


def main():

    rushHourBoard = get_board()

    # copy board for visualization purposes
    vizBoard = rushHourBoard.copy()

    algorithm = get_algorithm()
    
    if algorithm == 'randomise':
        moves = randomise(rushHourBoard)
    elif algorithm == 'breadth first':
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

    run_visualisation(vizBoard, moves)

    
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
            good_input = False
            while not good_input:
                try:
                    board_len = int(input('Type the board length (e.g. "6"): '))
                    if board_len > 4 and board_len <= 12:
                        good_input = True
                        continue
                except ValueError:
                    pass

                print('\nPlease enter an integer in the range 4 - 12.\n')

            rushHourBoard = Generate(board_len)
        else:
            continue
    
    return rushHourBoard


def get_algorithm():
    """
    Gets the algorithm from the user.
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
    Saves the best solution out of an inputted number of runs of the Randomise algorithm (see randomise.py for details)
    """
    print('\nRandomise gives the best result of a number of random runs.')
    good_input = False
    while not good_input:
        try:
            nr_runs = int(input('Number of random runs: '))
            if nr_runs > 0:
                good_input = True
                continue
        except ValueError:
            pass

    print('\nRandomise start', end='\n\n')
    start = time.perf_counter()

    best = float('inf')

    for i in range(nr_runs):
        new_model = rushHourBoard.copy()
        randomise = rd.Randomise(new_model)
        random_moves = randomise.run()

        if len(random_moves) < best:
            moves = random_moves
            best = len(random_moves)
    
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

        print('\nPlease enter a positive number.\n')

    print('\nDepth First start', end='\n\n')
    start = time.perf_counter()

    depth = df.DepthFirst(rushHourBoard)
    moves = depth.run(max_depth)

    finish = time.perf_counter()
    if len(moves) == 0: 
        pass
    else:
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
    print(f'Iterative Deepening found a solution in {len(moves) - 1} moves. See data.output.output.csv')
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

    # ask if user want to choose the parameters
    parameters = input('Do you want input custom parameters? (yes/no)')

    if parameters.lower() == 'yes':
        good_input = False
        while not good_input:
            try:
                random_nr = int(input('\nNumber of random algorithm runs, (recommended 1 - 1000): '))
                max_score = int(input('\nMaximum allowed heuristic score, (recommended 10 - 30): '))
                low_max_score = int(input('\nMaximum allowed heuristic score after failed A* search, (recommended 5 - 10): '))
                max_plus = int(input('\nIncrementation of the max. heuristic score after an A* iteration over the whole move set, (recommended 2 - 10): '))
                max_val = int(input('\nMaximum number of states one A* search is about to search, (recommended 500 - 10000): '))
                max_val_plus = int(input('\nIncrementation of the max. nr. of states to be searched after an A* iteration over the whole move set, (recommended 500 - 1500): '))

                if random_nr > 0 and max_score > 0 and low_max_score > 0:
                    good_input = True
                    continue
            except ValueError:
                pass
            
            print('\nPlease enter positive numbers.\n')
    else:
        # inputs for hill climber to find good solution, "emprically tested"
        random_nr = 50
        max_score = 6
        low_max_score = 3
        max_plus = 1
        max_val = 1000
        max_val_plus = 300   

    # ask how many runs they want to do
    print('\nThe best result of the Hill Climber runs will be exported to the output.csv file.')
    good_input = False
    while not good_input:
        try:
            nr_runs = int(input('Number of runs for the entire Hill climber: '))
            if nr_runs > 0:
                good_input = True
                continue
        except ValueError:
            pass
        
        print('Please input a positive number.')

    start = time.perf_counter()
    for run_number in range(nr_runs):
        board = rushHourBoard.copy()

        print(f'\nHill Climber start run {run_number + 1}') 
        start_hc = time.perf_counter()

        hillclimber = hc.Hillclimber(board)
        moveset = hillclimber.run(random_nr, max_score, max_plus, low_max_score, max_val, max_val_plus)

        finish_hc = time.perf_counter()
        print(f'Hill Climber run {run_number + 1} found solution in {len(moveset) - 1} moves.')
        print(f'runtime: {round(finish_hc - start_hc, 2)} seconds', end = '\n\n')

        if run_number == 0 or len(moveset) < len(moves):
            moves = moveset
    
    print(f"Hill Climber's best solution found was {len(moves) - 1} moves. See data.output.output.csv")        
    finish = time.perf_counter()
    print(f'runtime: {round(finish - start, 2)} seconds', end = '\n\n')

    return moves


def run_visualisation(vizBoard, moves):
    """
    Runs a visualisation in pygame.
    """
    good_input = False

    print('NOTE: Visualisation only possible when running on Windows (not on Linux/WSL).')

    while not good_input:
        visualise = input(' Do you want to visualise your solution? (yes/no): ')
        visualise = visualise.lower()
        if visualise == 'yes' or visualise == 'no':
            good_input = True
    
    if visualise == 'yes':
        print('NOTE: for visualisation, see pop-up pygame window')
        vizBoard.moves = moves[1:]
        viz = Visualizer(vizBoard)
        viz.run()


if __name__ == "__main__":
    main()



