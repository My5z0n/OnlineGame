import pygame
from Game_Entity import GameEntity, PlayerColors, rotate_point
from Wall import Wall


# Glowa klasa gracza
class GamePlayer(GameEntity):

    def __init__(self, color, x, y, id, bullet):
        super().__init__(1, pygame.Rect(x, y, 50, 50), color, x, y, id)
        self.lastconrol = {"w": 0, "a": 0, "s": 0, "d": 0, "r": 0, "l": 0, "f": 0}
        self.rotation = 0
        self.bullet = bullet
        self.health = 5

    def tick(self, gameEntitiesNonMovable, gameEntitiesMovable, gameOver):
        if gameOver is False:
            if self.health == 0:
                gameOver = True
                return gameOver

            self.pos += self.vel
            self.drawable.center = self.pos

            if self.lastconrol["r"]:
                self.rotation -= 1
            if self.lastconrol["l"]:
                self.rotation += 1

            for colid in gameEntitiesNonMovable:
                if colid != self:
                    if isinstance(colid, Wall) or isinstance(colid, GamePlayer):
                        if self.drawable.colliderect(colid.drawable):
                            self.pos -= self.vel
                            self.drawable.center = self.pos
            for colid in gameEntitiesMovable:
                if colid != self:
                    if isinstance(colid, Wall) or isinstance(colid, GamePlayer):
                        if self.drawable.colliderect(colid.drawable):
                            self.pos -= self.vel
                            self.drawable.center = self.pos

        return gameOver

    def update(self):
        self.vel.x = 0
        self.vel.y = 0
        if self.lastconrol["d"]:
            self.vel.x += 2
        if self.lastconrol["s"]:
            self.vel.y += 2
        if self.lastconrol["w"]:
            self.vel.y -= 2
        if self.lastconrol["a"]:
            self.vel.x -= 2
        if self.lastconrol["f"]:
            self.shoot()

    def shoot(self):
        dd = rotate_point(0, 0, self.rotation, (0, 1))
        self.bullet.set_start(int(dd[0] * 10), int(dd[1] * 10), self.drawable.center)

    def getdata(self):
        id = int(self.id)
        pos = self.pos
        color = self.color
        angle = self.rotation
        health = self.health
        return (id, pos, color, angle, health)

    def setdata(self, tuple):
        self.id = int(tuple[0])
        self.pos = tuple[1]
        self.color = tuple[2]
        self.drawable.center = self.pos
        self.rotation = tuple[3]
        self.health = tuple[4]

    def rotate(self, img, pos, angle):
        w, h = img.get_size()
        img2 = pygame.Surface((w * 2, h * 2), pygame.SRCALPHA)
        img2.blit(img, (w - pos[0], h - pos[1]))
        return pygame.transform.rotate(img2, angle)

    def draw(self, DISPLAY_SURFACE):
        pygame.draw.rect(DISPLAY_SURFACE, self.color.value, self.drawable)

        image_orig = pygame.Surface((25, 50))  # lufa
        image_orig.fill((200, 200, 200))
        image_orig.set_colorkey((0, 0, 0))
        new_image = self.rotate(image_orig, (12, 0), self.rotation)

        rect = new_image.get_rect()
        rect.center = (self.drawable.center[0], self.drawable.center[1])
        # pygame.draw.rect(DISPLAY_SURFACE, (200,200,200), rect)
        DISPLAY_SURFACE.blit(new_image, rect)

        if (self.health > 0):
            x = self.pos.x - 25
            y = self.pos.y - 40
            pygame.draw.rect(DISPLAY_SURFACE, (255, 0, 0), pygame.Rect(x, y, 50, 7), 0)
            pygame.draw.rect(DISPLAY_SURFACE, (0, 255, 0), pygame.Rect(x, y, self.health * 10, 7), 0)
        else:
            self.color = PlayerColors.GRAY
            font = pygame.font.Font("game_over.ttf", 72)
            text = font.render("Game Over", True, (255, 255, 255))
            text_rect = text.get_rect()
            text_x = 250 - text_rect.width / 2
            text_y = 250 - text_rect.height / 2
            DISPLAY_SURFACE.blit(text, [text_x, text_y])
