from code.classes.board import Board
<<<<<<< HEAD
from code.algorithms import randomise
=======
from code.classes.car import Car
from code.algorithms import randomise, greedy
>>>>>>> greedy_tryout
from code.output import output

def main():
<<<<<<< HEAD
    # init the board
    rushHourBoard = Board('./data/input/Rushhour6x6_1.csv')

    # solve the board using random moves and save it to the output file
    all_moves = randomise.run_milestone1(rushHourBoard, True)[0]
    output.export_to_csv(all_moves, './data/output/output.csv')
=======
    
    total_moves = 0

    for i in range(100):
        rushHourBoard = Board('./data/input/Rushhour6x6_3.csv')
        move_count = greedy.run(rushHourBoard)
        total_moves += move_count

    print(total_moves/100)

    # all_moves = randomise.run(rushHourBoard)

    # output.export_to_csv(all_moves, './data/output/output.csv')
    
    # rushHourBoard.update_matrix(-1,rushHourBoard.cars['A'])

    # rushHourBoard.print()

    # rushHourBoard.cars['P'].get_possibilities(rushHourBoard)

>>>>>>> greedy_tryout

    # average amount of steps for randomise to solve the board
    counters = 0
    maximum = 0 
    for i in range(100):
        rushHourBoard = Board('./data/input/Rushhour6x6_1.csv')
        counter = randomise.run_milestone1(rushHourBoard, False)[1]
        if counter > maximum:
            maximum = counter

        counters += counter
        
    print(f"[Baseline] The average amount of steps of 100 iterations is: {counters/100}")
    print(f"[Baseline] The maximum steps of 100 iterations is: {maximum}")
    

if __name__ == "__main__":
    main()
