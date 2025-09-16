import pygame
from os.path import join
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, bullet_group):
        super().__init__(groups)
        self.image = pygame.image.load(join("images", "player", "down", "0.png")).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 500
        self.bullet_group = bullet_group
        self.shoot_cooldown = 0.25
        self.time_since_last_shot = 0

    def input(self):
        keys = pygame.key.get_pressed()
        
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()
        
        self.shoot(keys)

    def shoot(self, keys):
        self.time_since_last_shot += self.dt
        if self.time_since_last_shot < self.shoot_cooldown:
            return

        direction = None
        if keys[pygame.K_UP]:
            direction = pygame.math.Vector2(0, -1)
        elif keys[pygame.K_DOWN]:
            direction = pygame.math.Vector2(0, 1)
        elif keys[pygame.K_LEFT]:
            direction = pygame.math.Vector2(-1, 0)
        elif keys[pygame.K_RIGHT]:
            direction = pygame.math.Vector2(1, 0)

        if direction:
            Bullet(self.rect.center, direction, self.bullet_group)
            self.time_since_last_shot = 0

    def move(self, dt):
        self.rect.center += self.direction * self.speed * dt

    def update(self, dt):
        self.dt = dt
        self.input()
        self.move(dt)
