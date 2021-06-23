# ACKNOWLEDGEMENT

from code.classes.model import Model

# hide pygame standard welcome message
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

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

        self.red = 222,0,0
        self.green = 0,255,0
        self.blue = 32,0,237
        self.black = 0,0,0
        self.yellow = 237,229,0

            
    def setup(self):
        """

        """
        pygame.init()
        screen = self.screen
        screen.fill((240,240,240)) # make background white
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
            pygame.event.get()
            car = self.model.board.cars[move[0]]
            self.model.update_matrix(car, move[1])
            self.setup()
            time.sleep(0.5)
        
        time.sleep(5)
        pygame.quit

