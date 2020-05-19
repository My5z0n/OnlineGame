import copy
import pickle
import queue
import time

import pygame, sys
from pygame.locals import *

from Game_Entity import PlayerColors
from Game_Player import GamePlayer
from Wall import Wall
import Bullet


class Game(object):

    def __init__(self, userInput1, userInput2, gameoutput):
        # Ustawiamy nasze kolejki od obu graczy
        # Zawieraja one sterowanie jakie wykonal gracz
        # w postaci slownika self.tmpcontrol = {"w": 0, "a": 0, "s": 0, "d": 0, "r": 0, "l": 0, "f": 0} }
        # gdzie 1 to wcisniety guzik a 0 brak wcisniecia
        self.gameOver = False
        self.idnum = 1
        self.userInput1 = userInput1
        self.userInput2 = userInput2
        self.gameoutput = gameoutput
        # maksymalna liczka klatek
        self.tps_max = 60.0

        # odpalamy srodowisko i tworzymy okno
        pygame.init()
        pygame.display.set_caption('HOST')
        print("Game Runs!")
        self.DISPLAY_SURFACE = pygame.display.set_mode((500, 500))

        # przydatne do okreslenia maksymalnej liczby klatek
        self.tps_clock = pygame.time.Clock()
        self.tps_delta = 0.0

        # tablice na wszystkie elementy gry
        self.gameEntitiesArray = []
        self.gamePlayersArray = []
        self.gameEntitiesNomovable = []

        self.tmpobj = Bullet.Bullet(PlayerColors.RED, 250, 250, 3)
        self.tmpobj.set_start(1, 0, (60, 60))
        self.gameEntitiesArray.append(self.tmpobj)
        # self.gameEntitiesNomovable.append(self.tmpobj)

        # dodajemy 1 gracza
        self.player1 = GamePlayer(PlayerColors.RED, 300, 60, 1, self.tmpobj)
        self.gameEntitiesArray.append(self.player1)
        self.gamePlayersArray.append(self.player1)
        self.idnum += 1

        self.tmpobj = Bullet.Bullet(PlayerColors.BLUE, 250, 250, 4)
        self.tmpobj.set_start(1, 0, (50, 50))
        self.gameEntitiesArray.append(self.tmpobj)
        # self.gameEntitiesNomovable.append(self.tmpobj)

        # dodajemy 2 gracza
        self.player2 = GamePlayer(PlayerColors.BLUE, 300, 440, 2, self.tmpobj)
        self.gameEntitiesArray.append(self.player2)
        self.gamePlayersArray.append(self.player2)

        # dodajemy sciany
        self.tmpobj = Wall(100, 100, 300, 20)
        self.gameEntitiesArray.append(self.tmpobj)
        self.gameEntitiesNomovable.append(self.tmpobj)

        self.tmpobj = Wall(100, 350, 300, 20)
        self.gameEntitiesArray.append(self.tmpobj)
        self.gameEntitiesNomovable.append(self.tmpobj)

        self.tmpobj = Wall(0, 0, 20, 500)
        self.gameEntitiesArray.append(self.tmpobj)
        self.gameEntitiesNomovable.append(self.tmpobj)

        self.tmpobj = Wall(480, 0, 20, 500)
        self.gameEntitiesArray.append(self.tmpobj)
        self.gameEntitiesNomovable.append(self.tmpobj)

        self.tmpobj = Wall(0, 0, 500, 20)
        self.gameEntitiesArray.append(self.tmpobj)
        self.gameEntitiesNomovable.append(self.tmpobj)

        self.tmpobj = Wall(0, 480, 500, 20)
        self.gameEntitiesArray.append(self.tmpobj)
        self.gameEntitiesNomovable.append(self.tmpobj)

        self.flag = -1

        self.timer = 0
        # Glowna petla gry tu dzieje sia cala gra
        while True:
            # sprawdzacz zdarzen i ich obslugi w tym wypatku tylko zamkniecie okna by dalo sie apke normalnie zamkac
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # W tej petli rzeczy sie dzieja w ograniczonej przez nas ilosci klatek na sekunde
            self.tps_delta += self.tps_clock.tick() / 1000.0
            while self.tps_delta > 1 / self.tps_max:
                self.tick()
                self.timer += 1
                if self.timer == 3:
                    self.send()
                    self.timer = 0

                self.tps_delta -= 1 / self.tps_max

            # Aktualizujemy graczy
            self.playerUpdate()
            # Czyscimy ekran i go wyswietlamy
            self.DISPLAY_SURFACE.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()

    # W tej funkcji aktualizujemy stan naszych graczy ktorzy u siebie wykonali swoje gory juz i musimy to zapdejtowac na hoscie
    def playerUpdate(self):
        # jezeli jest nowe wejscie od gracza to pobieramy to i aktualizujemy
        try:
            self.player1.lastconrol = self.userInput1.get(block=False)
            self.player1.update()
            self.flag = 1
        except queue.Empty:
            pass
        try:
            self.player2.lastconrol = self.userInput2.get(block=False)
            self.player2.update()
            self.flag = 1
        except queue.Empty:
            pass

    # tu rzeczy sie wynuja w scisle okreslonym tempie jak poruszanie
    def tick(self):
        if self.gameOver is False:
            for x in self.gameEntitiesArray:
                tmp = x.tick(self.gameEntitiesNomovable, self.gamePlayersArray, self.gameOver)
                if tmp is True:
                    self.gameOver = True
                    break

    def send(self):
        if self.flag == -1:
            try:
                self.gameoutput.put(self.gameEntitiesNomovable, block=False)
            except queue.Empty:
                raise Exception("Cos sie zepsulo przy wysylaniu array entity")
            self.flag = 0
        if self.flag == 1:
            try:
                array = []
                for x in self.gamePlayersArray:
                    xx = x.getdata()  # pobiera dane każdego gracza
                    array.append(xx)
                    xx = x.bullet.getdata()
                    array.append(xx)

                self.gameoutput.put((array, time.time()), block=False)
                # self.gameoutput.put(self.gamePlayersArray, block=False)

            except queue.Empty:
                raise Exception("Cos sie zepsulo przy wysylaniu array entity")

    # tu rysujemy wszystkie obiekty ktore powinny znalesc sie na naszej planszy
    def draw(self):
        for x in self.gameEntitiesArray:
            x.draw(self.DISPLAY_SURFACE)


# funkcja tylko do stworzenia klasy i jej odpalenia
def game(control1, control2, gameoutput):
    Game(control1, control2, gameoutput)
