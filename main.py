from code.classes.board import Board
from code.classes.car import Car
from code.algorithms import randomise
from code.algorithms import backtracking
from code.algorithms import depth
from code.algorithms import depth_first as df
from code.output import output

import timeit

# from code.algorithms import greedy as gr
# from code.visualisation import visualise as vis

def main():
    rushHourBoard = Board('./data/input/Rushhour6x6_1.csv')

    depth = df.DepthFirst(rushHourBoard)
    all_moves = depth.run()

    output.export_to_csv(all_moves, './data/output/output.csv')


    

if __name__ == "__main__":
    
    execution_time = timeit.timeit(main, number=1)
    print(f"Runtime of algorithm: {round(execution_time, 2)} seconds")
