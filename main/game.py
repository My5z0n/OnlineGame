import queue
import pygame, sys
from pygame.locals import *
import Game_Player as gp


class Game(object):

    def __init__(self, userInput1, userInput2):
        self.userInput1 = userInput1
        self.userInput2 = userInput2

        self.tps_max = 100.0

        pygame.init()
        pygame.display.set_caption('Hello World!')
        print("Game Runs!")
        self.DISPLAY_SURFACE = pygame.display.set_mode((500, 500))

        self.tps_clock = pygame.time.Clock()
        self.tps_delta = 0.0

        self.tmpcontrol={"w": 0, "a": 0, "s": 0, "d": 0}
        self.lastconrol2 = {"w": 0, "a": 0, "s": 0, "d": 0}

        self.player1 = gp.GamePlayer(self,gp.PlayerColors.RED)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.tps_delta += self.tps_clock.tick() / 1000.0
            while self.tps_delta > 1 / self.tps_max:
                self.tick()
                self.tps_delta -= 1 / self.tps_max
            self.playerUpdate()
            self.DISPLAY_SURFACE.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()

    def playerUpdate(self):
        try:
            self.player1.lastconrol = self.userInput1.get(block=False)
            self.player1.update()
        except queue.Empty:
            pass

    def tick(self):
        self.player1.tick()

    def draw(self):
        self.player1.draw()


def game(control1, control2):
    Game(control1, control2)
