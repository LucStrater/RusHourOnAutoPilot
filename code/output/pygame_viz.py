# ACKNOWLEDGEMENT

# hide pygame standard welcome message
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import time

class Game:
    """
    The Game class simulates the steps found by one of the algorithms. 
    """
    def __init__(self, model):
        self.model = model
        self.size = int(75) 
        self.boardSide = self.size * self.model.board.board_len
        self.screen = pygame.display.set_mode((self.boardSide,self.boardSide))
        self.colors = {}

        # vehicle colors
        self.red = 222,0,0
        self.green = 34,139,34
        self.blue = 32,0,237

            
    def setup(self):
        """
        Sets up the pygame, draws the map and places the cars. 
        For this it uses the inputs from the game solved by the desired algorithm.
        """
        pygame.init()
        screen = self.screen
        screen.fill((240,240,240)) 
        inter_car_gap = 10
        
        for car in self.model.board.cars.values():
            
            # get long and short side of the car
            long_side = int(((self.size*(car.length)) - inter_car_gap))
            short_side = self.size - inter_car_gap 

            # get car x and y coordinates in order to place car on the board
            position = self.model.get_car_pos(car)
            row, column = position[0], position[1]
            x = ((column)*self.size + (inter_car_gap / 2))
            y = ((row)*self.size + (inter_car_gap / 2))

            # place red car on the board
            if car.cid == 'X':
                image = pygame.Surface((long_side, short_side))
                sprite = pygame.draw.rect(image,self.red,(0,0,((self.size*(car.length))-inter_car_gap),(self.size - inter_car_gap)))
            
            # place trucks on the board
            elif car.length > 2:
                if car.orientation == "H":
                    image = pygame.Surface((long_side, short_side))
                    sprite = pygame.draw.rect(image, self.green, (0, 0, ((self.size*car.length)-inter_car_gap), (self.size - inter_car_gap)))
                else:
                    image = pygame.Surface((short_side, long_side))
                    sprite = pygame.draw.rect(image, self.green, (0, 0 ,(self.size - inter_car_gap), ((self.size*car.length) - inter_car_gap)))
            
            # place cars on the board
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
        Runs the pygame and makes all the car moves until the game is solved.
        """
        for move in self.model.moves:
            pygame.event.get()
            self.model.update_matrix(self.model.board.cars[move[0]], move[1])
            self.setup()
            time.sleep(0.5)
        
        time.sleep(5)
        pygame.quit
