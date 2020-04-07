import pygame
from Game_Entity import GameEntity
from Wall import Wall


#Glowa klasa gracza
class GamePlayer(GameEntity):

    def __init__(self, color, x, y):
        super().__init__(1, pygame.Rect(x, y, 50, 50), color, x, y)
        self.lastconrol = {"w": 0, "a": 0, "s": 0, "d": 0}

    def tick(self, gameEntitiesNonMovable, gameEntitiesMovable):
        self.pos += self.vel
        self.drawable.center = self.pos

        for colid in gameEntitiesNonMovable:
            if colid != self:
                if isinstance(colid, Wall) or isinstance(colid, GamePlayer):
                    if self.drawable.colliderect(colid.drawable):
                        self.pos -=self.vel
                        self.drawable.center = self.pos
        for colid in gameEntitiesMovable:
            if colid != self:
                if isinstance(colid, Wall) or isinstance(colid, GamePlayer):
                    if self.drawable.colliderect(colid.drawable):
                        self.pos -=self.vel
                        self.drawable.center = self.pos

    def update(self):
        self.vel.x = 0
        self.vel.y = 0
        if self.lastconrol["d"]:
            self.vel.x += 4
        if self.lastconrol["s"]:
            self.vel.y += 4
        if self.lastconrol["w"]:
            self.vel.y -= 4
        if self.lastconrol["a"]:
            self.vel.x -= 4

