import copy
from code.algorithms.a_star import A_star
import operator

class Pruned_a_star(A_star):
    """
    A pruned A* algorithm that finds a suboptimal solution of a rush hour board.
    """

    def create_children(self, state):
        moves = []
        scores = []
        
        if len(state.moves) > 10: 
            # make child from current board without deepcopying
            for car in state.cars.values():
                car_possibilities = car.get_possibilities(state)

                # for every car loop over its possible moves
                for move in car_possibilities:
                    state.update_matrix(move, state.cars[car.car_id])

                    matrix_tuple = tuple([tuple(i) for i in state.matrix])
                    # calculate heuristic score for child
                    # save move-to-child + heuristic score in dictionary (or sth)
                    # if current matrix exists in archive, and moves to get to current matrix is shorter, replace board in archive
                    if matrix_tuple not in self.closed.keys():
                        moves.append((move, car.car_id))
                        scores.append(self.calculate_h3_score(state))

                    # reverse to parent board state
                    state.update_matrix(move * -1, state.cars[car.car_id])
            
            sorted_moves = [x for _,x in sorted(zip(scores,moves))]
            
            for move in sorted_moves[:3]:
                new_board = copy.deepcopy(state)

                # update new board with chosen move
                new_board.update_matrix(move[0], new_board.cars[move[1]])

                # append move made to list of moves to get to incumbent (new) board
                new_board.add_move(new_board.cars[move[1]].car_id, move[0])

                # For matrix form, turn list of lists into tuple of tuples, such that matrix is hashable
                matrix_tuple = tuple([tuple(i) for i in new_board.matrix])

                # if this state has not been reached put it on the stack
                if (matrix_tuple not in self.closed.keys() and matrix_tuple not in self.open.keys()):
                    new_board.score = self.calculate_h3_score(new_board)
                    self.open[matrix_tuple] = new_board

                # if current matrix exists in archive, and moves to get to current matrix is shorter, replace board in archive
                elif matrix_tuple in self.closed.keys():
                    if len(new_board.moves) < len(self.closed[matrix_tuple].moves):
                        self.closed[matrix_tuple].moves = new_board.moves

                # same as above, but for open
                elif matrix_tuple in self.open.keys():
                    if len(new_board.moves) < len(self.open[matrix_tuple].moves):
                        self.open[matrix_tuple].moves = new_board.moves

        else:
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

                    # For matrix form, turn list of lists into tuple of tuples, such that matrix is hashable
                    matrix_tuple = tuple([tuple(i) for i in new_board.matrix])

                    # if this state has not been reached put it on the stack
                    if (matrix_tuple not in self.closed.keys() and matrix_tuple not in self.open.keys()):
                        new_board.score = self.calculate_h3_score(new_board)
                        # new_board.score_two = self.calculate_h4_score(state, new_board)
                        # new_board.score_three = self.calculate_h5_score(new_board)
                        # new_board.score_four = self.calculate_h6_score(new_board)
                        self.open[matrix_tuple] = new_board

                    # if current matrix exists in archive, and moves to get to current matrix is shorter, replace board in archive
                    elif matrix_tuple in self.closed.keys():
                        if len(new_board.moves) < len(self.closed[matrix_tuple].moves):
                            self.closed[matrix_tuple].moves = new_board.moves

                    # same as above, but for open
                    elif matrix_tuple in self.open.keys():
                        if len(new_board.moves) < len(self.open[matrix_tuple].moves):
                            self.open[matrix_tuple].moves = new_board.moves