from code.classes.board import Board
from code.classes.car import Car
from code.algorithms import randomise
# from code.algorithms import greedy as gr
# from code.visualisation import visualise as vis

def main():
    rushHourBoard = Board('./data/Rushhour6x6_1.csv')

    randomise.run(rushHourBoard)
    
    # rushHourBoard.update_matrix(-1,rushHourBoard.cars['A'])

    # rushHourBoard.print()

    # rushHourBoard.cars['P'].get_possibilities(rushHourBoard)
    

if __name__ == "__main__":
    main()
