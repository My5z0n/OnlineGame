import queue
import pygame, sys
from pygame.locals import *

from Game_Entity import PlayerColors
from Game_Player import GamePlayer
from Wall import Wall


class Game(object):

    def __init__(self, userInput1, userInput2):
        # Ustawiamy nasze kolejki od obu graczy
        # Zawieraja one sterowanie jakie wykonal gracz
        # w postaci slownika self.tmpcontrol = {"w": 0, "a": 0, "s": 0, "d": 0}
        # gdzie 1 to wcisniety guzik a 0 brak wcisniecia
        self.userInput1 = userInput1
        self.userInput2 = userInput2

        # maksymalna liczka klatek
        self.tps_max = 100.0

        # odpalamy srodowisko i tworzymy okno
        pygame.init()
        pygame.display.set_caption('HOST')
        print("Game Runs!")
        self.DISPLAY_SURFACE = pygame.display.set_mode((500, 500))

        # przydatne do okreslenia maksymalnej liczny klatek
        self.tps_clock = pygame.time.Clock()
        self.tps_delta = 0.0

        # tablice na wszystkie elementy gry
        self.gameEntitiesArray = []
        self.gamePlayersArray = []

        # dodajemy 1 gracza
        self.player1 = GamePlayer(self, PlayerColors.RED, 300, 60)
        self.gameEntitiesArray.append(self.player1)
        self.gamePlayersArray.append(self.player1)

        # dodajemy 2 gracza
        self.player2 = GamePlayer(self, PlayerColors.BLUE, 300, 440)
        self.gameEntitiesArray.append(self.player2)
        self.gamePlayersArray.append(self.player2)

        # dodajemy sciany
        self.tmpobj = Wall(self, 100, 100, 300, 20)
        self.gameEntitiesArray.append(self.tmpobj)

        self.tmpobj = Wall(self, 100, 350, 300, 20)
        self.gameEntitiesArray.append(self.tmpobj)

        self.tmpobj = Wall(self, 0, 0, 20, 500)
        self.gameEntitiesArray.append(self.tmpobj)

        self.tmpobj = Wall(self, 480, 0, 20, 500)
        self.gameEntitiesArray.append(self.tmpobj)

        self.tmpobj = Wall(self, 0, 0, 500, 20)
        self.gameEntitiesArray.append(self.tmpobj)

        self.tmpobj = Wall(self, 0, 480, 500, 20)
        self.gameEntitiesArray.append(self.tmpobj)

        #Glowna petla gry tu dzieje sia cala gra
        while True:
            #sprawdzacz zdarzen i ich obslugi w tym wypatku tylko zamkniecie okna by dalo sie apke normalnie zamkac
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # W tej petli rzeczy sie dzieja w ograniczonej przez nas ilosci klatek na sekunde
            self.tps_delta += self.tps_clock.tick() / 1000.0
            while self.tps_delta > 1 / self.tps_max:
                self.tick()
                self.tps_delta -= 1 / self.tps_max

            #Aktualizujemy graczy
            self.playerUpdate()
            #Czyscimy ekran i go wyswietlamy
            self.DISPLAY_SURFACE.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()

    #W tej funkcji aktualizujemy stan naszych graczy ktorzy u siebie wykonali swoje gory juz i musimy to zapdejtowac na hoscie
    def playerUpdate(self):
        #jezeli jest nowe wejscie od gracza to pobieramy to i aktualizujemy
        try:
            self.player1.lastconrol = self.userInput1.get(block=False)
            self.player1.update()
        except queue.Empty:
            pass
        try:
            self.player2.lastconrol = self.userInput2.get(block=False)
            self.player2.update()
        except queue.Empty:
            pass

    # tu rzeczy sie wynuja w scisle okreslonym tempie jak poruszanie
    def tick(self):
        for x in self.gameEntitiesArray:
            x.tick()

    # tu rysujemy wszystkie obiekty ktore powinny znalesc sie na naszej planszy
    def draw(self):
        for x in self.gameEntitiesArray:
            x.draw()

#funkcja tylko do stworzenia klasy i jej odpalenia
def game(control1, control2):
    Game(control1, control2)
