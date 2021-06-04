from code.classes.board import Board
from code.algorithms import randomise
from code.output import output

def main():
    # init the board
    rushHourBoard = Board('./data/input/Rushhour6x6_1.csv')

    # solve the board using random moves and save it to the output file
    all_moves = randomise.run_milestone1(rushHourBoard, True)[0]
    output.export_to_csv(all_moves, './data/output/output.csv')

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
