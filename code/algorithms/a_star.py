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

    class A_star():
        """
        An A* algorithm that finds the optimal solution of a rush hour board.
        """
        def __init__(self, board):
            self.board = board

            # initialise the open / closed list
            self.open = {}
            self.open[tuple([tuple(i) for i in self.board.matrix])] = copy.deepcopy(self.board)

            self.closed = {}

        def get_next_state(self):
            """
            Method that gets the board with the lowest score from open
            """
            sorted_list = list(self.open.values()).sort(key=self.calculate_h1_score)
            return sorted_list.pop(0)


        def calculate_h1_score(self, state):
            return state.matrix[state.cars['X'].row][state.cars['X'].column] - state.matrix[state.cars['X'].row][state.board_len - 1]


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
                    if matrix_tuple not in self.closed.keys() and matrix_tuple not in self.open.keys():
                        self.open[matrix_tuple] = new_board
                        
                    # if current matrix exists in archive, and moves to get to current matrix is shorter, add current matrix to archive
                    elif matrix_tuple in self.closed.keys() and len(new_board.moves) < self.closed.get(matrix_tuple, None):
                        self.closed[matrix_tuple] = new_board

                    elif matrix_tuple in self.open.keys() and len(new_board.moves) < self.open.get(matrix_tuple, None):
                        self.open[matrix_tuple] = new_board


        def move_backtracking():
