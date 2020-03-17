import pygame
from enum import Enum
from pygame.math import Vector2
from Game_Entity import GameEntity, PlayerColors


#Sciana jak jest kazdy widzi
class Wall(GameEntity):

    def __init__(self, game, x, y, w, h):
        super().__init__(game, 0,pygame.Rect(x, y, w, h),PlayerColors.WHITE,x,y)

    def tick(self):
        pass

    def draw(self):
        pygame.draw.rect(self.game.DISPLAY_SURFACE, self.color.value, self.drawable)
