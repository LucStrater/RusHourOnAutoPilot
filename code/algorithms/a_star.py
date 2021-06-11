"""

// A* Search Algorithm
1.  Initialize the open list
2.  Initialize the closed list
    put the starting node on the open 
    list (you can leave its f at zero)

3.  while the open list is not empty
    a) find the node with the least f on 
       the open list, call it "q"

    b) pop q off the open list
  
    c) generate q's 8 successors and set their 
       parents to q
   
    d) for each successor
        i) if successor is the goal, stop search
          successor.g = q.g + distance between 
                              successor and q
          successor.h = distance from goal to 
          successor (This can be done using many 
          ways, we will discuss three heuristics- 
          Manhattan, Diagonal and Euclidean 
          Heuristics)
          
          successor.f = successor.g + successor.h

        ii) if a node with the same position as 
            successor is in the OPEN list which has a 
           lower f than successor, skip this successor

        iii) if a node with the same position as 
            successor  is in the CLOSED list which has
            a lower f than successor, skip this successor
            otherwise, add  the node to the open list
     end (for loop)
  
    e) push q on the closed list
    end (while loop)

    """

import copy


class A_star:
    """
    An A* algorithm that finds the optimal solution of a rush hour board.
    """

    def __init__(self, board):
        self.board = board

        # initialise the open / closed list
        self.open = {}
        self.open[tuple([tuple(i) for i in self.board.matrix])] = copy.deepcopy(self.board)

        self.closed = {}
        self.closed[tuple([tuple(i) for i in self.board.matrix])] = copy.deepcopy(self.board)

    def get_next_state(self):
        """
        Method that gets the board with the lowest score from open
        """
        score = float("inf")
        len_board = float("inf")
        next_state = None
        for board in self.open.values():
            # h1 is okay, h2 is bad, h3 is
            test = self.calculate_h3_score(board)
            if test < score:
                score = test
                next_state = tuple([tuple(i) for i in board.matrix])
                len_board = len(board.moves)
            elif test == score and len(board.moves) < len_board:
                next_state = tuple([tuple(i) for i in board.matrix])
                len_board = len(board.moves)

        return self.open.pop(next_state)

    def calculate_h1_score(self, state):
        return state.board_len - 2 - state.cars["X"].column

    def calculate_h2_score(self, state):
        filled_spots = 0

        # for each spot on the row of car X, check if it is filled
        for i in range(state.board_len):
            if state.matrix[state.cars["X"].row][i] is not None:
                filled_spots += 1

        return filled_spots

    def calculate_h3_score(self, state):
        score = 0
        len_board = range(state.board_len)
        # for each spot on the row of car X, check if it is filled
        for i in len_board:
            unique = []
            if (state.matrix[state.cars["X"].row][i] is not None and state.matrix[state.cars["X"].row][i] != "X"):
                for j in len_board:
                    if state.matrix[j][i] is not None:
                    # if state.matrix[j][i] is not None and state.matrix[j][i] not in unique:
                        # score += 1
                        # unique.append(state.matrix[j][i])


                        blocking_car = state.matrix[state.cars["X"].row][i]
                        if state.matrix[j][i] == blocking_car:
                            continue
                        elif state.cars[state.matrix[j][i]].orientation == 'V':
                          if state.cars[state.matrix[j][i]].length == 2:
                              j += 2
                              score += 1
                          else:
                              j += 3
                              score += 1
                        else:
                            score += 1

        return score

    def create_children(self, state):
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
                    self.open[matrix_tuple] = new_board

                # if current matrix exists in archive, and moves to get to current matrix is shorter, add current matrix to archive
                elif matrix_tuple in self.closed.keys():
                    # print(self.closed[matrix_tuple])
                    if len(new_board.moves) < len(self.closed[matrix_tuple].moves):
                        self.closed[matrix_tuple] = new_board

                elif matrix_tuple in self.open.keys():
                    if len(new_board.moves) < len(self.open[matrix_tuple].moves):
                        self.open[matrix_tuple] = new_board

    def move_backtracking(self, solution_state):
        optimal_moveset = []
        while True:
            optimal_moveset.insert(0, solution_state.moves.pop())

            if solution_state.matrix == self.board.matrix:
                break

            move = -optimal_moveset[0][1]
            car = solution_state.cars[optimal_moveset[0][0]]
            solution_state.update_matrix(move, car)
            solution_state.moves = self.closed[tuple([tuple(i) for i in solution_state.matrix])].moves

        return optimal_moveset

    def run(self):

        # repeat untill the stack is empty
        while True:
            # take the board at the top of the stack
            state = self.get_next_state()

            if state.is_solution():
                break

            # save states to archive
            self.closed[tuple([tuple(i) for i in state.matrix])] = state

            # create children
            self.create_children(state)

        solution = self.move_backtracking(state)

        # return the best solution found
        # return solution
        return solution
