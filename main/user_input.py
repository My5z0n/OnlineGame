import copy
import queue
import time

import pygame
import sys
from pygame.locals import *

from Bullet import Bullet
from Game_Entity import PlayerColors
from Game_Player import GamePlayer


class Game(object):

    def __init__(self, control1, control2, hostoutput):
        # Ustawiamy nasze kolejki od obu graczy
        # Zawieraja one sterowanie jakie wykonal gracz
        # w postaci slownika self.tmpcontrol = {"w": 0, "a": 0, "s": 0, "d": 0, "r": 0, "l": 0, "f": 0}
        # gdzie 1 to wcisniety guzik a 0 brak wcisniecia
        self.control1 = control1
        self.control2 = control2
        self.hostoutput = hostoutput
        # maksymalna liczka klatek
        self.tps_max = 60.0

        self.lastcontrol = {"w": 0, "a": 0, "s": 0, "d": 0, "r": 0, "l": 0, "f": 0}
        self.data_array = []
        self.nowdata = None
        # odpalamy srodowisko i tworzymy okno
        pygame.init()
        pygame.display.set_caption('CLIENT')
        print("Game Runs!")
        self.DISPLAY_SURFACE = pygame.display.set_mode((500, 500))

        # przydatne do okreslenia maksymalnej liczny klatek
        self.tps_clock = pygame.time.Clock()
        self.tps_delta = 0.0

        # tablice na wszystkie elementy gry
        self.gameEntitiesArray = []
        self.gamePlayersArray = []
        self.gameEntitiesNonmovable = []

        # pocisk
        self.bullet = Bullet(PlayerColors.RED, 250, 250, 3)
        self.gameEntitiesArray.append(self.bullet)
        self.gamePlayersArray.append(self.bullet)

        # gracz referencyjny
        self.player = GamePlayer(PlayerColors.RED, 300, 60, 0, self.bullet)
        self.gameEntitiesArray.append(self.player)
        self.gamePlayersArray.append(self.player)

        self.flag = 0
        self.mydata = None
        self.lastupdate = 0

        # Glowna petla gry tu dzieje sia cala gra
        while True:
            # sprawdzacz zdarzen i ich obslugi w tym wypatku tylko zamkniecie okna by dalo sie apke normalnie zamkac
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.getfromhost()
            # W tej petli rzeczy sie dzieja w ograniczonej przez nas ilosci klatek na sekunde
            self.tps_delta += self.tps_clock.tick() / 1000.0
            while self.tps_delta > 1 / self.tps_max:
                self.tick()
                self.tps_delta -= 1 / self.tps_max

            # Czyscimy ekran i go wyswietlamy
            self.DISPLAY_SURFACE.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()

    # tu rzeczy sie wynuja w scisle okreslonym tempie jak poruszanie
    def getfromhost(self):
        if self.flag == 0:
            try:
                data = self.hostoutput.get(block=False)
                self.gameEntitiesNonmovable = data
            except queue.Empty:
                pass
            self.flag = 1
        else:
            try:
                data = self.hostoutput.get(block=False)
                self.data_array.append(data)
            except queue.Empty:
                pass

    # tu rzeczy sie wynuja w scisle okreslonym tempie jak poruszanie
    def tick(self):
        changed = 0
        keys = pygame.key.get_pressed()
        if self.lastcontrol["d"] != keys[pygame.K_d]:
            self.lastcontrol["d"] = keys[pygame.K_d]
            changed = 1
        if self.lastcontrol["a"] != keys[pygame.K_a]:
            self.lastcontrol["a"] = keys[pygame.K_a]
            changed = 1
        if self.lastcontrol["s"] != keys[pygame.K_s]:
            self.lastcontrol["s"] = keys[pygame.K_s]
            changed = 1
        if self.lastcontrol["w"] != keys[pygame.K_w]:
            self.lastcontrol["w"] = keys[pygame.K_w]
            changed = 1
        if self.lastcontrol["r"] != keys[pygame.K_RIGHT]:
            self.lastcontrol["r"] = keys[pygame.K_RIGHT]
            changed = 1
        if self.lastcontrol["l"] != keys[pygame.K_LEFT]:
            self.lastcontrol["l"] = keys[pygame.K_LEFT]
            changed = 1
        if self.lastcontrol["f"] != keys[pygame.K_SPACE]:
            self.lastcontrol["f"] = keys[pygame.K_SPACE]
            changed = 1

        if changed:
            print("Wysylam sygnal od usera z klawiatury:")
            print(self.lastcontrol)
            try:
                self.control1.put(self.lastcontrol, block=False)
            except queue.Empty:
                raise Exception("Cos sie zepsulo")

    # for x in self.gamePlayersArray:
    #  x.tick(self.gameEntitiesNonmovable,self.gamePlayersArray)

    # tu rysujemy wszystkie obiekty ktore powinny znalesc sie na naszej planszy
    def draw(self):
        for x in self.gameEntitiesNonmovable:
            x.draw(self.DISPLAY_SURFACE)

        if len(self.data_array) != 0:  # odebraliśmy nową informacje od hosta
            if self.data_array[0][1] + 0.2 <= time.time():  # timestamp z opóźnieniem 0.2
                self.nowdata = self.data_array.pop(0)  # aktualna informacja
            elif self.nowdata is not None:
                nowdata3 = self.data_array[
                    0]  # wstawiamy nową daną, której nie rysujemy bo za wcześnie względem opóźnienia
                nowdata2 = copy.copy(self.nowdata)  # zostawiamy kopie tej informacji
                for i in range(len(nowdata2[0])):
                    if nowdata2[0][i][0] == nowdata3[0][i][0]:  # [0] - array, [i] - ity element, [0] - id
                        if nowdata2[0][i][0] == 3 or nowdata2[0][i][0] == 4:
                            nowdata2[0][i] = (nowdata2[0][i][0], nowdata2[0][i][1], nowdata2[0][i][2],
                                              nowdata3[0][i][3])  # przekopiowujemy informacje o exists
                        nowdata2[0][i][1].x = int((nowdata2[0][i][1].x + nowdata3[0][i][1].x) / 2)  # [0][i][1] - pos
                        nowdata2[0][i][1].y = int((nowdata2[0][i][1].y + nowdata3[0][i][1].y) / 2)

                self.nowdata = nowdata2

        if self.nowdata is not None:  # jest nowa informacja
            for xxx in self.nowdata[0]:  # iterujemy po tablicy array z hosta (czyli wszystkie informacje o graczach)
                if xxx[0] == 1 or xxx[0] == 2:  # porównujemy id, 1 i 2 to player
                    self.player.setdata(xxx)
                    self.player.draw(self.DISPLAY_SURFACE)

                if xxx[0] == 3 or xxx[0] == 4:
                    self.bullet.setdata(xxx)
                    self.bullet.draw(self.DISPLAY_SURFACE)


# funkcja tylko do stworzenia klasy i jej odpalenia
def game2(control1, control2, hostinput):
    Game(control1, control2, hostinput)
