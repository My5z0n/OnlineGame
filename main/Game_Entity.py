import uuid
from math import sin, cos, radians

import pygame
from enum import Enum
from pygame.math import Vector2


# kolory by wyswietlic ale gownie z mysla o rozpoznawaniu typu czy 1 czy 2 gracz itd.
class PlayerColors(Enum):
    RED = (199, 8, 8)
    BLUE = (8, 62, 199)
    WHITE = (250, 250, 250)


def rotate_point(cx, cy, angle, p):
    s = sin((-1)*radians(angle))
    c = cos((-1)*radians(angle))

    px = p[0]
    py = p[1]
    px -= cx
    py -= cy

    xnew = px * c - py * s
    ynew = px * s + py * c
    px = xnew + cx
    py = ynew + cy
    return px, py


# abstakcyjna klasa wszystkie obekty w grze dziedzicza po niej
class GameEntity:
    def __init__(self, movable, drawable, color, x, y, id, exists=1):
        self.id = id
        self.drawable = drawable
        self.pos = Vector2(x, y)
        self.vel = Vector2(0, 0)
        self.movable = movable
        self.color = color
        self.exists = exists

    def draw(self, DISPLAY_SURFACE):
        pygame.draw.rect(DISPLAY_SURFACE, self.color.value, self.drawable)

    def tick(self, gameEntitiesNonMovable, gameEntitiesMovable):
        pass
