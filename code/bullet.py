# bullet.py
import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, groups, speed=700):
        super().__init__(groups)
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        self.image.fill(pygame.Color("yellow"))
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction.normalize() if hasattr(direction, "length") and direction.length() != 0 else pygame.Vector2(0,0)
        self.speed = speed

    def update(self, dt):
        # move using vector math then set rect.center with ints
        pos = pygame.Vector2(self.rect.center) + self.direction * self.speed * dt
        self.rect.center = (int(pos.x), int(pos.y))

        # remove if outside screen
        if (
            self.rect.right < 0 or self.rect.left > 1280
            or self.rect.bottom < 0  or self.rect.top > 800
        ):
            self.kill()
