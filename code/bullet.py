import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, groups, speed=700):
        super().__init__(groups)
        self.image = pygame.Surface((10, 10))
        self.image.fill("yellow")
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.speed = speed

    def update(self, dt):
        
        self.rect.center += self.direction * self.speed * dt
        # ako e nadvor od ekrano
        if (
            self.rect.right < 0 or self.rect.left > 1280
            or self.rect.bottom < 0  or self.rect.top > 800
        ):
            self.kill()
