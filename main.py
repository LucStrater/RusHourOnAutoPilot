from code.classes.board import Board
from code.classes.car import Car
from code.algorithms import randomise
from code.output import output
# from code.algorithms import greedy as gr
# from code.visualisation import visualise as vis

def main():
    # rushHourBoard = Board('./data/input/Rushhour6x6_1.csv')

    counters = 0
    maximum = 0 
    for i in range(100):
        rushHourBoard = Board('./data/input/Rushhour6x6_1.csv')
        counter = randomise.run(rushHourBoard)
        if counter > maximum:
            maximum = counter

        counters += counter
        
    print(f"The average amount of steps of 100 iterations is: {counters/100}")
    print(f"The maximum steps of 100 iterations is: {maximum}")
    # all_moves = randomise.run(rushHourBoard)

    # output.export_to_csv(all_moves, './data/output/output.csv')
    
    # rushHourBoard.update_matrix(-1,rushHourBoard.cars['A'])

    # rushHourBoard.print()

    # rushHourBoard.cars['P'].get_possibilities(rushHourBoard)


    

if __name__ == "__main__":
    main()
