# power.py
import pygame
from os.path import join

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, pos, groups, power_type):
        super().__init__(groups)
        self.type = power_type
        self.image = pygame.image.load(join("images", f"{power_type}.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect(center=pos)

    def apply(self, player):
        # shoot_cooldown is in seconds
        if self.type == "fast_shoot":
            # reduce cooldown by 0.15s, clamp to a sensible minimum
            player.shoot_cooldown = max(0.05, player.shoot_cooldown - 0.15)
        elif self.type == "small":
            # set player scale (player handles rescaling frames)
            player.set_scale(0.6)
        elif self.type == "damage":
            player.damage += 1
        self.kill()
