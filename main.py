from code.classes.board import Board
from code.classes.car import Car
from code.algorithms import randomise, greedy, breadth
from code.output import output
from sys import argv
import time

def main():
    # get board title from the terminal
    if len(argv) not in [1, 2]:
        print("Usage: python3 main.py [filename (example: <6x6_1>)]")
        exit(1)
    
    if len(argv) == 2:
        board_title = f"./data/input/Rushhour{argv[1]}.csv"
    else:
        board_title = './data/input/Rushhour4x4_0.csv'


    board = Board(board_title)

    start = time.perf_counter()
    breadth.run(board)
    finish = time.perf_counter()

    print(f'runtime: {round(finish - start, 2)} seconds')
    
    









    # # solve the board using random moves and print first 10 moves
    # all_moves = randomise.run_milestone1(rushHourBoard, True)[0]

    # # save moves to output file
    # output.export_to_csv(all_moves, './data/output/output.csv')

    # # average amount of steps for 100 iterations of randomise to solve the board
    # counters = 0
    # maximum = 0 
    # for i in range(100):
    #     rushHourBoard = Board(board_title)
    #     counter = randomise.run_milestone1(rushHourBoard, False)[1]
    #     if counter > maximum:
    #         maximum = counter

    #     counters += counter
        
    # print("[Baseline: make random moves until solved]")
    # print(f"The average amount of steps of 100 iterations is: {counters/100}")
    # print(f"The maximum steps of 100 iterations is: {maximum}")
    # print()

    # # average amount of steps for 100 iterations of greedy 1 to solve the board
    # counters_greedy_1 = 0
    # maximum_greedy_1 = 0 
    # for i in range(100):
    #     rushHourBoard = Board(board_title)
    #     counter_greedy_1 = greedy.run_1(rushHourBoard)
    #     if counter_greedy_1 > maximum_greedy_1:
    #         maximum_greedy_1 = counter_greedy_1

    #     counters_greedy_1 += counter_greedy_1

    # print("[Greedy 1: if row of car X is empty -> finish]")
    # print(f"The average amount of steps of 100 iterations is: {counters_greedy_1/100}")
    # print(f"The maximum steps of 100 iterations is: {maximum_greedy_1}")
    # print(f"That is {round(- (counters_greedy_1/counters - 1) * 100)}% better than the baseline")
    # print()

    # # average amount of steps for 100 iterations of greedy 2 to solve the board
    # counters_greedy_2 = 0
    # maximum_greedy_2 = 0 
    # for i in range(100):
    #     rushHourBoard = Board(board_title)
    #     counter_greedy_2 = greedy.run_2(rushHourBoard)
    #     if counter_greedy_2 > maximum_greedy_2:
    #         maximum_greedy_2 = counter_greedy_2

    #     counters_greedy_2 += counter_greedy_2
        
    # print("[Greedy 2: if cars on row of car X can all be moved -> move them + Greedy 1]")
    # print(f"The average amount of steps of 100 iterations is: {counters_greedy_2/100}")
    # print(f"The maximum steps of 100 iterations is: {maximum_greedy_2}")
    # print(f"That is {round(- (counters_greedy_2/counters - 1) * 100)}% better than the baseline")
    # print()


    # # average amount of steps for 100 iterations of greedy 3 to solve the board
    # counters_greedy_3 = 0
    # maximum_greedy_3 = 0 
    # for i in range(100):
    #     rushHourBoard = Board(board_title)
    #     counter_greedy_3 = greedy.run_3(rushHourBoard)
    #     if counter_greedy_3 > maximum_greedy_3:
    #         maximum_greedy_3 = counter_greedy_3

    #     counters_greedy_3 += counter_greedy_3
        
    # print("[Greedy 3: if Greedy 1 & 2 not possible, try randomly move a car that blocks road for car X]")
    # print(f"The average amount of steps of 100 iterations is: {counters_greedy_3/100}")
    # print(f"The maximum steps of 100 iterations is: {maximum_greedy_3}")
    # print(f"That is {round(- (counters_greedy_3/counters - 1) * 100)}% better than the baseline")


if __name__ == "__main__":
    main()
