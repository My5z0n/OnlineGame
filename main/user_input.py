import queue
import pygame, sys
from pygame.locals import *

from Game_Entity import PlayerColors
from Game_Player import GamePlayer
from Wall import Wall


class Game(object):

    def __init__(self, control1, control2, hostoutput):
        # Ustawiamy nasze kolejki od obu graczy
        # Zawieraja one sterowanie jakie wykonal gracz
        # w postaci slownika self.tmpcontrol = {"w": 0, "a": 0, "s": 0, "d": 0}
        # gdzie 1 to wcisniety guzik a 0 brak wcisniecia
        self.control1 = control1
        self.control2 = control2
        self.hostoutput = hostoutput
        # maksymalna liczka klatek
        self.tps_max = 60.0

        self.lastcontrol = {"w": 0, "a": 0, "s": 0, "d": 0}

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

        self.flag = 0

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
                self.getfromhost()
                self.tick()
                self.tps_delta -= 1 / self.tps_max

            # Czyscimy ekran i go wyswietlamy
            self.DISPLAY_SURFACE.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()

    # tu rzeczy sie wynuja w scisle okreslonym tempie jak poruszanie
    def getfromhost(self):
        if self.flag ==0:
            try:
                data = self.hostoutput.get(block=False)
                self.gameEntitiesNonmovable = data
                self.flag=1


            except queue.Empty:
                pass
            try:
                data = self.hostoutput.get(block=False)
                self.gamePlayersArray = data

            except queue.Empty:
                pass
        else:
            try:
                data = self.hostoutput.get(block=False)
                self.gamePlayersArray = data

            except queue.Empty:
                pass

    # tu rzeczy sie wynuja w scisle okreslonym tempie jak poruszanie
    def tick(self):
        self.getfromhost()
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

        if changed:
            print("Wysylam sygnal od usera z klawiatury:")
            print(self.lastcontrol)
            try:
                self.control1.put(self.lastcontrol, block=False)
            except queue.Empty:
                raise Exception("Cos sie zepsulo")


        for x in self.gamePlayersArray:
            x.tick(self.gameEntitiesNonmovable,self.gamePlayersArray)

    # tu rysujemy wszystkie obiekty ktore powinny znalesc sie na naszej planszy
    def draw(self):
        for x in self.gameEntitiesNonmovable:
            x.draw(self.DISPLAY_SURFACE)
        for x in self.gamePlayersArray:
            x.draw(self.DISPLAY_SURFACE)



# funkcja tylko do stworzenia klasy i jej odpalenia
def game2(control1, control2, hostinput):
    Game(control1, control2, hostinput)
