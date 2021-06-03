import random
import time

def random_move(board):
    random_car_possibilities = []

    while len(random_car_possibilities) == 0:
        # pick random car
        random_car = random.choice(list(board.cars.values()))

        # get possibilities
        random_car_possibilities = random_car.get_possibilities(board)

        
    # make random move
    random_move = random.choice(random_car_possibilities)
    board.update_matrix(random_move, random_car)
    
def run(board):
    print('In run')
    while board.is_solution:
        print("In loop")
        random_move(board)
        board.print()
        time.sleep(5)

 