import pygame
from Game_Entity import GameEntity, PlayerColors
from Game_Player import GamePlayer
from Wall import Wall


# Glowa klasa gracza
class Bullet(GameEntity):

    def __init__(self, color, x, y, id):
        super().__init__(1, pygame.Rect(x, y, 15, 15), color, x, y, id)
        self.lastconrol = {"w": 0, "a": 0, "s": 0, "d": 0, "r": 0, "l": 0, "f": 0}
        self.exists = 1

    def tick(self, gameEntitiesNonMovable, gameEntitiesMovable):
        if self.exists!=0:
            self.pos += self.vel
            self.drawable.center = self.pos


            for colid in gameEntitiesNonMovable:
                if colid != self:
                    if isinstance(colid, Wall) or isinstance(colid, GamePlayer):
                        if self.drawable.colliderect(colid.drawable):
                            self.exists=0
                            self.pos  = (5,5)
                            self.drawable.center = self.pos
            for colid in gameEntitiesMovable:
                if colid != self:
                    if isinstance(colid, Wall) or isinstance(colid, GamePlayer):
                        if self.drawable.colliderect(colid.drawable):
                            if self.color!=colid.color:
                                self.exists = 0
                                print("Hit!")
                                self.pos = (5, 5)
                                self.drawable.center = self.pos
    def set_start(self,x,y,pos):
        self.vel.x = x
        self.vel.y = y
        self.exists = 1
        self.pos=pos
    # def update(self):
    #     self.vel.x = 0
    #     self.vel.y = 0
    #     if self.lastconrol["d"]:
    #         self.vel.x += 2
    #     if self.lastconrol["s"]:
    #         self.vel.y += 2
    #     if self.lastconrol["w"]:
    #         self.vel.y -= 2
    #     if self.lastconrol["a"]:
    #         self.vel.x -= 2


    def getdata(self):
        id = int(self.id)
        pos = self.pos
        color = self.color

        return (id, pos, color)

    def setdata(self, tuple):
        self.id = int(tuple[0])
        self.pos = tuple[1]
        self.color = tuple[2]
        self.drawable.center = self.pos



    def draw(self, DISPLAY_SURFACE):
        pygame.draw.rect(DISPLAY_SURFACE, self.color.value, self.drawable)

