import pygame
import os
import random 
from pygame.locals import *

class Mon(pygame.sprite.Sprite):

    def __init__(self, game, x, y, color):
        self.groups = game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.images = []


        back=[]
        forward=[]
        left=[]
        right=[]
        for i in range(1, 4):
          img = pygame.image.load('pokemon/back' + str(i) + '.png').convert()
          ALPHA = (0, 0, 0)
          img.convert_alpha()     # optimise
          img.set_colorkey(ALPHA)
          back.append(img)
        self.images.append(back)

        for i in range(1, 4):
          img = pygame.image.load('pokemon/forward' + str(i) + '.png').convert()
          ALPHA = (0, 0, 0)
          img.convert_alpha()     # optimise
          img.set_colorkey(ALPHA)
          forward.append(img)
        self.images.append(forward)

        for i in range(1, 4):
          img = pygame.image.load('pokemon/left' + str(i) + '.png').convert()
          ALPHA = (0, 0, 0)
          img.convert_alpha()     # optimise
          img.set_colorkey(ALPHA)
          left.append(img)
        self.images.append(left)

        for i in range(1, 4):
          img = pygame.image.load('pokemon/right' + str(i) + '.png').convert()
          ALPHA = (0, 0, 0)
          img.convert_alpha()     # optimise
          img.set_colorkey(ALPHA)
          right.append(img)
        self.images.append(right)

        self.facing = "forward"






