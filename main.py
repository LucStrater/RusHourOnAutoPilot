from code.classes.board import Board
from code.classes.car import Car
from code.algorithms import randomise
from code.output import output
# from code.algorithms import greedy as gr
# from code.visualisation import visualise as vis

def main():
    rushHourBoard = Board('./data/input/Rushhour6x6_1.csv')

    all_moves = randomise.run(rushHourBoard)

    output.export_to_csv(all_moves, './data/output/output.csv')
    
    # rushHourBoard.update_matrix(-1,rushHourBoard.cars['A'])

    # rushHourBoard.print()

    # rushHourBoard.cars['P'].get_possibilities(rushHourBoard)


    

if __name__ == "__main__":
    main()
