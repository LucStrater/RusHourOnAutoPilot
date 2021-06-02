
class Board():
    def __init__(self, source_file):
        self.matrix = self.load_matrix(source_file)
    

    def load_matrix(self, source_file):
        """
        Load all vehicles into the board.
        """
        matrix = []

        # get board length
        board_length = int(source_file.strip("/data/Rushhour").split('x')[0])

        print(board_length)

        
        # fill board with None

        # for all cars in the csv file create the car and put on board

        # with open(source_file, 'r') as in_file:
        #     reader = csv.DictReader(in_file)

        #     for row in reader:
        #         nodes[row['id']] = Node(row['id'], row['id'])

        return matrix


    def is_solution(self):
        """
        Check if the current configuration is a solution. 
        """
        pass