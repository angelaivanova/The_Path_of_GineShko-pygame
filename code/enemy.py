# enemy.py
import pygame
from os.path import join
from os import walk
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, pos, groups, bullet_group, player):
        super().__init__(groups)
        self.enemy_type = enemy_type
        self.bullet_group = bullet_group
        self.player = player

        self.raw_frames = []
        self.frames = []
        self.load_images(enemy_type)
        self.frame_index = 0.0
        self.image = self.frames[0] if self.frames else pygame.Surface((32,32), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)

        self.health = 3 if enemy_type == "bat" else 5 if enemy_type == "skeleton" else 4
        self.speed = 160 if enemy_type == "bat" else 100 if enemy_type == "skeleton" else 80
        self.anim_speed = 6

    def load_images(self, enemy_type):
        folder = join("images", "enemies", enemy_type)
        found = False
        for folder_path, _, file_names in walk(folder):
            if file_names:
                found = True
                for file_name in sorted(file_names, key=lambda n: int(n.split('.')[0])):
                    surf = pygame.image.load(join(folder_path, file_name)).convert_alpha()
                    self.frames.append(surf)
        if not found:
            # placeholder so things don't crash
            surf = pygame.Surface((32,32), pygame.SRCALPHA)
            pygame.draw.rect(surf, (255,0,0), surf.get_rect(), 1)
            self.frames.append(surf)

    def animate(self, dt):
        if not self.frames:
            return
        self.frame_index += self.anim_speed * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0.0
        self.image = self.frames[int(self.frame_index)]

    def move(self, dt):
        if self.player:
            direction = pygame.Vector2(self.player.rect.center) - pygame.Vector2(self.rect.center)
            if direction.length_squared() > 0:
                direction = direction.normalize()
                new_pos = pygame.Vector2(self.rect.center) + direction * self.speed * dt
                self.rect.center = (int(new_pos.x), int(new_pos.y))

    def check_bullet_collision(self):
        if self.bullet_group is None:
            return
        hits = pygame.sprite.spritecollide(self, self.bullet_group, dokill=True)
        if hits:
            self.health -= len(hits)
            if self.health <= 0:
                self.kill()

    def check_player_collision(self):
        if self.player and self.rect.colliderect(self.player.rect):
            self.player.take_damage()

    def update(self, dt):
        self.animate(dt)
        self.move(dt)
        self.check_bullet_collision()
        self.check_player_collision()
