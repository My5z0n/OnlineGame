import pygame
from pygame.math import Vector2


class GamePlayer:

    def __init__(self, game):
        self.lastconrol = {"w": 0, "a": 0, "s": 0, "d": 0}
        self.game = game
        self.box = pygame.Rect(10, 10, 50, 50)
        self.color = (0, 150, 255)
        self.pos = Vector2(10, 10)
        self.vel = Vector2(0, 0)

    def tick(self):
        self.pos += self.vel
        self.box.center = self.pos

    def update(self):
        self.vel.x=0
        self.vel.y=0
        if self.lastconrol["d"]:
            self.vel.x += 4
        if self.lastconrol["s"]:
            self.vel.y += 4
        if self.lastconrol["w"]:
            self.vel.y -= 4
        if self.lastconrol["a"]:
            self.vel.x -= 4

    def draw(self):
        pygame.draw.rect(self.game.DISPLAY_SURFACE, self.color, self.box)
