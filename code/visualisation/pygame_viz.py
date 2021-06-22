# ACKNOWLEDGEMENT


from code.classes.model import Model
import pygame
import sys
import math
import random
import time

class Game:

    def __init__(self, model):
        self.model = model
        self.size = int(100) 
        self.boardSide = self.size * self.model.board.board_len
        self.screen = pygame.display.set_mode((self.boardSide,self.boardSide))
        self.colors = {}

        self.red = 255,0,0
        self.green = 0,255,0
        self.blue = 0,0,255
        self.black = 0,0,0
        self.yellow = 255,255,0

            
    def setup(self):
        """

        """
        pygame.init()
        screen = self.screen
        screen.fill((255,255,255)) # make background white
        count = 0
        inter_car_gap = 10
        
        for car in self.model.board.cars.values():

            long_side = int(((self.size*(car.length)) - inter_car_gap))
            short_side = self.size - inter_car_gap 
            position = self.model.get_car_pos(car)
            row, column = position[0], position[1]
            x = ((column)*self.size + (inter_car_gap / 2))
            y = ((row)*self.size + (inter_car_gap / 2))

            # RED CAR  -->  if car.cid == 'X'
            if car.cid == 'X':
                image = pygame.Surface((long_side, short_side))
                sprite = pygame.draw.rect(image,self.red,(0,0,((self.size*(car.length))-inter_car_gap),(self.size - inter_car_gap)))
            
            # TRUCKS
            elif car.length > 2:
                if car.orientation == "H":
                    image = pygame.Surface((long_side, short_side))
                    sprite = pygame.draw.rect(image, self.yellow, (0, 0, ((self.size*car.length)-inter_car_gap), (self.size - inter_car_gap)))
                else:
                    image = pygame.Surface((short_side, long_side))
                    sprite = pygame.draw.rect(image, self.yellow, (0, 0 ,(self.size - inter_car_gap), ((self.size*car.length) - inter_car_gap)))
            
            # CARS
            else:
                if car.orientation == "H":
                    image = pygame.Surface((long_side, short_side))
                    sprite = pygame.draw.rect(image,self.blue,(0,0,((self.size*car.length) - inter_car_gap),(self.size - inter_car_gap)))
                else:
                    image = pygame.Surface((short_side, long_side))
                    sprite = pygame.draw.rect(image,self.blue,(0,0,(self.size - inter_car_gap),((self.size * car.length) - inter_car_gap)))
                    
            screen.blit(image,(x,y))
        pygame.display.update()


    def run(self):
        """

        """
        for move in self.model.moves:
            car = self.model.board.cars[move[0]]
            self.model.update_matrix(car, move[1])
            self.setup()
            time.sleep(0.5)
        
        time.sleep(5)
        pygame.quit

#============================================================================================================================#
#creating a new Car class that will be used to make our "car" objects
# class Car:
#     #initializing
#     def __init__(self, name, orient, long, rowPos, colPos):
#         self.name = name
#         self.orient = str(orient)
#         self.long = int(long) 
#         self.rowPos = int(rowPos)
#         self.colPos = int(colPos)
#         self.front = int(self.frontOfCar() )
#         self.rear = int(self.backOfCar())

#     #function to determine the back of the cars
#     def backOfCar(self):
#         if self.orient == "v":
#             return self.rowPos
#         else:
#             return self.colPos

#     #function to determine the front of the car
#     def frontOfCar(self):
#         if self.orient == "v":
#             return (self.rowPos + (int(self.long) ))
#         else:
#             return (self.colPos + (int(self.long) ))

    
#creating the game class that will be the core aspect of the game.
#this will import the puzzle, check legallities and actually move the cars
# class Game:
#     #initializing
#     def __init__(self):
#         self.listOfCars = self.loadGame()
#         self.allCars = []
#         # base our bord on the input board_len (maybe only used for terminal viz)
#         self.board = [
#             [" ¤ "," ¤ "," ¤ "," ¤ "," ¤ "," ¤ "],
#             [" ¤ "," ¤ "," ¤ "," ¤ "," ¤ "," ¤ "],
#             [" ¤ "," ¤ "," ¤ "," ¤ "," ¤ "," ¤ "],
#             [" ¤ "," ¤ "," ¤ "," ¤ "," ¤ "," ¤ "],
#             [" ¤ "," ¤ "," ¤ "," ¤ "," ¤ "," ¤ "],
#             [" ¤ "," ¤ "," ¤ "," ¤ "," ¤ "," ¤ "]
#             ]
#         self.red = 255,0,0
#         self.green = 0,255,0
#         self.blue = 0,0,255
#         self.black = 0,0,0
#         self.yellow = 255,255,0
#         self.size = int(100)
#         self.boardSide = self.size * 6 #input board_len
#         self.screen = pygame.display.set_mode((self.boardSide,self.boardSide))
#         self.listOfSprites = []

        
    #function that will load the game file and put the contents in it into a list    
    # def loadGame(self):
    #     gameFile = open(sys.argv[1],"r") # file contains following columns: orientation,length,row,col: we have ID,orientation,length,col,row 
    #     content = gameFile.readlines()
    #     gameFile.close()
    #     for x in range(len(content)):
    #         content[x].replace("\n","")
    #     return content #content returns a list of strings, ['h, 2, 2, 0\n', 'v, 2, 0, 0\n']

    #sets up the GUI so the game looks nice


#this fucntion is used to get mouse inputs from the player and decipher what the player has clicked on
#this is then used to get the coords of the new position that the player wants the car to be in
#these new coords are then returned and can be used by the isLegal() function

# we dont need this function, we already have car,nCol,nRow !
    # def movement(self):
    #     complete = False
    #     marker = 0
    #     target = None
    #     while complete == False:
    #         ev = pygame.event.get()
    #         for event in ev:
    #             if event.type == pygame.QUIT:
    #                 pygame.quit
    #             elif event.type == pygame.MOUSEBUTTONDOWN:
    #                 if marker == 0:
    #                     marker = 1
    #                     origin = pygame.mouse.get_pos()
    #                     originX = origin[0] // 100
    #                     originY = origin[1] // 100
    #                     if self.board[originY][originX] != " ¤ ":
    #                         target = int(self.board[originY][originX])
    #                         car = self.allCars[target]
    #                         num = int(car.name)
    #                     else:
    #                         marker = 0
    #                         print("please click on a car")
    #                 elif marker == 1:
    #                     newPos = pygame.mouse.get_pos()
    #                     nCol = newPos[0] // 100
    #                     nRow = newPos[1] // 100
    #                     return car,nCol,nRow


    #function to create car objects with all the aspects outlined in the game file
    # useless
    # def addCar(self,name,orient,long,rowPos,colPos):
    #     return Car(name,orient,long,rowPos,colPos)


    #function that will take all the cars that we have created and add them all together into one list
    # def carGen(self):
    #     for x in range(len(self.listOfCars)):
    #         self.listOfCars[x].replace("\n","")
    #         spec = self.listOfCars[x].split(",")
    #         orient = spec[0]
    #         long = spec[1]
    #         rowPos = spec[2]
    #         colPos = spec[3]

    #         newCar = self.addCar(x,orient,long,rowPos,colPos)

    #         self.allCars.append(newCar)


    #function to update the board with the cars and their positions
    # def updateBoard(self):
    #     for car in self.allCars:
    #         if car.orient == "h":                
    #             for x in range(int(car.long)):
    #                 if car.name <10:
    #                     self.board[int(car.rowPos)][int(car.colPos)+x] = " "+str(car.name)+" "
    #                     # for aligned viz in terminal, doesnt matter for us (AND we use letters, so nproblem)
    #                 elif car.name >= 10:
    #                     self.board[int(car.rowPos)][int(car.colPos)+x] = str(car.name)+" "
    #         elif car.orient == "v":
    #             for x in range(int(car.long)):
    #                 if car.name <10:
    #                     self.board[int(car.rowPos)+x][int(car.colPos)] = " "+str(car.name)+" "
    #                 elif car.name >= 10:
    #                     self.board[int(car.rowPos)+x][int(car.colPos)] = str(car.name)+" "


    #fucntion to check the legallity of the player's moves
    #checks to make sur ethe car wont go out of the board and that there are no cars in the way of the move
    #useless, we only do legal moves
    # def isLegal(self,carnum,newRow,newCol):
    #     nRow = int(newRow)
    #     nCol = int(newCol)
    #     car = self.allCars[carnum]
    #     deltaR = int(nRow - car.rowPos)
    #     deltaC = int(nCol - car.colPos)
    #     if car.orient == "h":
    #         if nRow != car.rowPos:
    #             return 0
    #         elif deltaC > 0:
    #             for i in range(int(deltaC)):
    #                 if self.board[car.rowPos][(car.rear + ( 1 + i ))] != " ¤ ":
    #                     if int(self.board[car.rowPos][(car.rear + ( 1 + i ))]) == int(car.name):
    #                         pass
    #                     else:
    #                         return 0
    #                 elif (car.colPos + (deltaC)) > 6:
    #                     return 0
    #                 else:
    #                     return 1
    #         elif deltaC < 0:
    #             for i in range(int(math.fabs(deltaC))):
    #                 if self.board[car.rowPos][(car.colPos - ( 1 + i ))] != " ¤ ":
    #                     if int(self.board[car.rowPos][(car.colPos - ( 1 + i ))]) == int(car.name):
    #                         pass
    #                     else:
    #                         return 0
    #                 elif (car.colPos + (deltaC)) < 0:
    #                     return 0
    #                 else:
    #                     return 1        
    #     elif car.orient == "v":
    #         if nCol != car.colPos:
    #             return 0
    #         elif deltaR > 0:
    #             for i in range(int(deltaR)):
    #                 if self.board[(car.rowPos + (car.long -1 ) + ( 1 + i ))][(car.colPos)] != " ¤ ":
    #                     if int(self.board[(car.rowPos + (car.long -1 ) + ( 1 + i ))][(car.colPos)]) == int(car.name):
    #                         pass
    #                     else:
    #                         return 0
    #                 elif (car.rowPos + (deltaR)) > 6:
    #                     return 0
    #                 else:
    #                     return 1
    #         elif deltaR < 0:
    #             for i in range(int(math.fabs(deltaR))):
    #                 if self.board[car.rowPos - ( 1 + i )][(car.colPos)] != " ¤ ":
    #                     if int(self.board[car.rowPos - ( 1 + i )][(car.colPos)]) == int(car.name):
    #                         pass
    #                     else:
    #                         return 0
    #                 elif (car.rowPos + (deltaR)) < 0:
    #                     return 0
    #                 else:
    #                     return 1
                        
    #function to remover the cars from the previous list so they can be moved to a new spot  
    # change old position to none and replace the car on the board 
    # def removeCar(self,carnum):
    #     car = self.allCars[carnum]
    #     if car.orient == "h":                
    #         for x in range(int(car.long)):
    #             self.board[int(car.rowPos)][int(car.colPos)+x] = " ¤ "
    #     elif car.orient == "v":
    #         for x in range(int(car.long)):
    #             self.board[int(car.rowPos)+x][int(car.colPos)] = " ¤ "

    #function to see if the game is over
    # is_solution()
    # def endGame(self):
    #     car = self.allCars[0]
    #     if (car.colPos + ((car.long) -1 )) == 5:
    #         return 1
    #     else:
    #         return 0

#function to move cars as long as the move is legal
# in moveCar input the car,newCol and newRow we get from the list of moves
    # def moveCar(self):
    #     car,newCol,newRow = self.movement()
    #     num = int(car.name)
    #     if self.isLegal(num,newRow,newCol) == 1: #
    #         deltaR = newRow - car.rowPos #
    #         deltaC = newCol - car.colPos #
    #         deltaRfront = newRow - (car.rowPos + ( car.long - 1)) #
    #         deltaCfront = newCol - (car.colPos + (car.long - 1)) #
    #         if car.orient == "h":
    #             if deltaC > 0:
    #                 self.removeCar(num)
    #                 car.colPos += (deltaCfront)  # car.colPos = newCol
    #                 self.updateBoard()
    #             elif deltaC < 0: #
    #                 self.removeCar(num) #
    #                 car.colPos += (deltaC) #
    #                 self.updateBoard() #
    #         elif car.orient == "v":
    #             if deltaR > 0:
    #                 self.removeCar(num)
    #                 car.rowPos += (deltaRfront) # car.rowPos = newRow
    #                 self.updateBoard()
    #             elif deltaR < 0: #
    #                 self.removeCar(num) #
    #                 car.rowPos += (deltaR) #
    #                 self.updateBoard() #
    #     else: #
    #         print("INVALID MOVE") #

    
#main            
# if __name__ == "__main__":

#     if len(sys.argv) != 2:
#         sys.stderr.write("usage: () game_file.txt\n")
#         sys.exit()
#     TrafficJam = Game()
#     TrafficJam.play()




    

