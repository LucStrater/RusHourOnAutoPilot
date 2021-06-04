from code.classes.board import Board
from code.classes.car import Car
from code.algorithms import randomise
from code.output import output
# from code.algorithms import greedy as gr
# from code.visualisation import visualise as vis

def main():
    # rushHourBoard = Board('./data/input/Rushhour6x6_1.csv')

    total_moves = 0
    max_moves = 0

    for i in range(1000):
        rushHourBoard = Board('./data/input/Rushhour6x6_3.csv')
        move_count = randomise.run(rushHourBoard)
        total_moves += move_count
        
        if move_count > max_moves:
            max_moves = move_count
        
    # print(f"The average amount of steps of 100 iterations is: {counters/100}")
    # print(f"The maximum steps of 100 iterations is: {maximum}")
    print(f'avg of 1000 was:\n    {total_moves/1000}\nmax number of steps was:\n    {max_moves}')

    # all_moves = randomise.run(rushHourBoard)

    # output.export_to_csv(all_moves, './data/output/output.csv')
    
    # rushHourBoard.update_matrix(-1,rushHourBoard.cars['A'])

    # rushHourBoard.print()

    # rushHourBoard.cars['P'].get_possibilities(rushHourBoard)


    

if __name__ == "__main__":
    main()
