import uuid
import pygame
from enum import Enum
from pygame.math import Vector2

#kolory by wyswietlic ale gownie z mysla o rozpoznawaniu typu czy 1 czy 2 gracz itd.
class PlayerColors(Enum):
    RED = (199, 8, 8)
    BLUE = (8, 62, 199)
    WHITE = (250,250,250)

#abstakcyjna klasa wszystkie obekty w grze dziedzicza po niej
class GameEntity:
    def __init__(self,game,movable,drawable,color,x,y,exists=1):
        self.game = game
        self.id=uuid.uuid1()
        self.drawable=drawable
        self.pos = Vector2(x, y)
        self.vel = Vector2(0, 0)
        self.movable=movable
        self.color=color
        self.exists=exists

    def draw(self):
        pygame.draw.rect(self.game.DISPLAY_SURFACE, self.color.value, self.drawable)

    def tick(self):
        pass
