import queue

import pygame, sys
from pygame.locals import *


def game2(control1, control2):
    max_tps = 70.0

    pygame.init()
    DISPLAY_SURFACE = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Hello World!')
    box1 = pygame.Rect(10, 10, 50, 50)
    box2 = pygame.Rect(10, 10, 50, 50)
    clock = pygame.time.Clock()
    delta = 0.0
    lastconrol = {"w": 0, "a": 0, "s": 0, "d": 0}
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        delta += clock.tick() / 1000.0
        while delta > 1 / max_tps:
            delta -= 1 / max_tps

            changed = 0
            keys = pygame.key.get_pressed()
            if lastconrol["d"] != keys[pygame.K_d]:
                lastconrol["d"] = keys[pygame.K_d]
                changed = 1
            if lastconrol["a"] != keys[pygame.K_a]:
                lastconrol["a"] = keys[pygame.K_a]
                changed = 1
            if lastconrol["s"] != keys[pygame.K_s]:
                lastconrol["s"] = keys[pygame.K_s]
                changed = 1
            if lastconrol["w"] != keys[pygame.K_w]:
                lastconrol["w"] = keys[pygame.K_w]
                changed = 1

            if changed:
                print("Wysylam sygnal od usera z klawiatury:")
                print(lastconrol)
                try:
                    control1.put(lastconrol, block=False)
                except queue.Empty:
                    raise Exception("Cos sie zepsulo")