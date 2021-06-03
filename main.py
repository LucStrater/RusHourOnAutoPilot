from code.classes.board import Board
from code.classes.car import Car
# from code.algorithms import randomise
# from code.algorithms import greedy as gr
# from code.visualisation import visualise as vis

def main():
    rushHourBoard = Board('./data/Rushhour6x6_3.csv')
    rushHourBoard.print()

    # print(rushHourBoard.cars['A'].get_possibilities(rushHourBoard))

    rushHourBoard.get_options_all_cars()
    

if __name__ == "__main__":
    main()
