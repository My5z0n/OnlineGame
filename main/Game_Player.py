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

    def tick(self, gameEntitiesNonMovable, gameEntitiesMovable):
        self.pos += self.vel
        self.drawable.center = self.pos

        if self.lastconrol["r"]:
            self.rotation += 1
        if self.lastconrol["l"]:
            self.rotation -= 1

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
        pos = (self.drawable.center[0], self.drawable.center[1] - 50)
        dd = rotate_point(0, 0, self.rotation, (0,1))
        self.bullet.set_start(int(dd[0]*10),int(dd[1]*10),self.drawable.center)

    def getdata(self):
        id = int(self.id)
        pos = self.pos
        color = self.color
        angle = self.rotation

        return (id, pos, color, angle)

    def setdata(self, tuple):
        self.id = int(tuple[0])
        self.pos = tuple[1]
        self.color = tuple[2]
        self.drawable.center = self.pos
        self.rotation = tuple[3]

    def rotate(self, img, pos, angle):
        w, h = img.get_size()
        img2 = pygame.Surface((w * 2, h * 2), pygame.SRCALPHA)
        img2.blit(img, (w - pos[0], h - pos[1]))
        return pygame.transform.rotate(img2, angle)

    def draw(self, DISPLAY_SURFACE):
        pygame.draw.rect(DISPLAY_SURFACE, self.color.value, self.drawable)
        image_orig = pygame.Surface((25, 50))
        image_orig.fill((200, 200, 200))
        image_orig.set_colorkey((0, 0, 0))
        new_image = self.rotate(image_orig, (12, 0), self.rotation)

        rect = new_image.get_rect()
        rect.center = (self.drawable.center[0], self.drawable.center[1])
        # pygame.draw.rect(DISPLAY_SURFACE, (200,200,200), rect)
        DISPLAY_SURFACE.blit(new_image, rect)
