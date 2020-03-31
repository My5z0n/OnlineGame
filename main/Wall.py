import pygame
from enum import Enum
from pygame.math import Vector2
from Game_Entity import GameEntity, PlayerColors


#Sciana jak jest kazdy widzi
class Wall(GameEntity):

    def __init__(self, x, y, w, h):
        super().__init__(0,pygame.Rect(x, y, w, h),PlayerColors.WHITE,x,y)

    def tick(self, gameEntitiesNonMovable, gameEntitiesMovable):
        pass

