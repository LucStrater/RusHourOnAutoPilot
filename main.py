from code.classes.board import Board
from code.classes.car import Car
from code.algorithms import randomise, greedy
from sys import argv
from code.algorithms import depth_first as df
from code.algorithms import iterative_deepening as id
from code.algorithms import a_star as ast
from code.algorithms import breadth as bf
from code.output import output
import time


def main():
    # get board title from the terminal
    if len(argv) not in [1, 2, 3]:
        print("Usage: python3 main.py [filename (example: <6x6_1>)]")
        exit(1)

    if len(argv) == 2:
        board_title = f"./data/input/Rushhour{argv[1]}.csv"
    else:
        board_title = './data/input/Rushhour6x6_1.csv'

    # init the board
    rushHourBoard = Board(board_title)

    ########################### A* ##############################
    start = time.perf_counter()

    a_star = ast.A_star(rushHourBoard)
    moves = a_star.run()
    print(f"best solution for A*: {moves}. This takes {len(moves) - 1} moves.")

    finish = time.perf_counter()
    print(f'runtime: {round(finish - start, 2)} seconds')
    # ########################### Breadth first ###########################
    # bf_start = time.perf_counter()

    # breadth_first = bf.Breadth_first(rushHourBoard)
    # bf_moves = breadth_first.run()
    # print(f"best solution for breadth first: {bf_moves}. This takes {len(bf_moves) - 1} moves.")

    # bf_finish = time.perf_counter()

    # print(f'runtime: {round(bf_finish - bf_start, 2)} seconds')

    # ########################### Depth first ###########################

    # start = time.perf_counter()

    # depth = df.DepthFirst(rushHourBoard)
    # all_moves = depth.run()
    # print(
    #     f"best solution for depth first: {all_moves}. This takes {len(all_moves) - 1} moves.")

    # # output.export_to_csv(all_moves, './data/output/output.csv')

    # finish = time.perf_counter()
    # print(f'runtime depth first: {round(finish - start, 2)} seconds')

    # ######################## Iterative deepening #####################
    # start = time.perf_counter()

    # depth = id.Iterative_deepening(rushHourBoard)
    # all_moves = depth.run()
    # print(f"best solution for iterative deepening: {all_moves}. This takes {len(all_moves) - 1} moves.")

    # # output.export_to_csv(all_moves, './data/output/output.csv')

    # finish = time.perf_counter()
    # print(f'runtime iterative deepening: {round(finish - start, 2)} seconds')

    # ############################# Random ################################

    # # solve the board using random moves and print first 10 moves
    # # all_moves = randomise.run_milestone1(rushHourBoard, True)[0]

    # # save moves to output file
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


if __name__ == "__main__":

    main()
