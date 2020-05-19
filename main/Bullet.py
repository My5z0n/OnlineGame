import pygame
from Game_Entity import GameEntity, PlayerColors
from Game_Player import GamePlayer
from Wall import Wall
from pygame.math import Vector2

# Glowa klasa gracza
class Bullet(GameEntity):

    def __init__(self, color, x, y, id):
        super().__init__(1, pygame.Rect(x, y, 15, 15), color, x, y, id)
        self.lastconrol = {"w": 0, "a": 0, "s": 0, "d": 0, "r": 0, "l": 0, "f": 0}
        self.exists = 1

    def tick(self, gameEntitiesNonMovable, gameEntitiesMovable, gameOver):
        if self.exists != 0:
            self.pos += self.vel
            self.drawable.center = self.pos

            for colid in gameEntitiesNonMovable:
                if colid != self:
                    if isinstance(colid, Wall) or isinstance(colid, GamePlayer):
                        if self.drawable.colliderect(colid.drawable):
                            self.exists = 0
                            self.pos = (5, 5)
                            self.drawable.center = self.pos
            for colid in gameEntitiesMovable:
                if colid != self:
                    if isinstance(colid, Wall) or isinstance(colid, GamePlayer):
                        if self.drawable.colliderect(colid.drawable):
                            if self.color != colid.color:
                                self.exists = 0
                                print("Hit!")
                                colid.health -= 1
                                self.pos = (5, 5)
                                self.drawable.center = self.pos

    def set_start(self, x, y, pos):
        self.vel.x = x
        self.vel.y = y
        self.exists = 1
        self.pos = pos


    def getdata(self):
        id = int(self.id)
        pos = self.pos
        color = self.color
        exists = self.exists
        return (id, Vector2(pos), color,exists)

    def setdata(self, tuple):
        self.id = int(tuple[0])
        self.pos = tuple[1]
        self.color = tuple[2]
        self.drawable.center = self.pos
        self.exists = tuple[3]

    def draw(self, DISPLAY_SURFACE):
        if self.exists:
            pygame.draw.rect(DISPLAY_SURFACE, self.color.value, self.drawable)
