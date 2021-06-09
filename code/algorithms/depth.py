import copy
import time

def depth_run(board):

    # add current board to list
    depth = 137
    stack = []
    stack.append(board)
    archive = []
    archiveX = []
    solutions = []
    while len(stack) > 0:
        state = stack.pop()

        if state.is_solution():
            solutions.append(state.moves)
            print(state.moves)

        # if length of list of moves is smaller than depth, create new boards at deeper level 
        if len(state.moves) < depth:

            # get current possibilities of all cars on board
            for car in state.cars.values():
                car_possibilities = car.get_possibilities(state)
                
                # for every car loop over its possible moves
                for move in car_possibilities:
                    # copy the board of the previous board
                    new_board = copy.deepcopy(state)

                    # update new board with chosen move
                    new_board.update_matrix(move, new_board.cars[car.car_id])
                    
                    # append move made to list of moves to get to incumbent (new) board
                    new_board.add_move(new_board.cars[car.car_id].car_id, move)

                    # proofed working but needs to append matrices below
                    if new_board.matrix not in archive:
                        stack.append(new_board)

                    # if new_board.matrix in archive:
                    #     if len(new_board.moves) < len(archiveX[new_board.matrix in archive].moves):
                            

                    #     elif len(new_board.moves) > len(old_board.moves):


                    # # all_matrices = list(map((lambda x: x.matrix), archive))
                    # # print(all_matrices)
                    
                    # if new_board in archive:      
                    #     for board in archiveX:
                    #         if new_board.matrix == board.matrix:
                    #             if len(new_board.matrix) < len(board.matrix):
                    #                 if new_board.moves == board.moves[:len(new_board.moves) + 1]:
                                        
                                        
                            

            archive.append(state.matrix)
            # archiveX.append(state)

    solutions.sort(key=len)

    # print(solutions[0])
    return solutions[0] 