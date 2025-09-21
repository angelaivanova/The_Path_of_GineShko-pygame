# player.py
import pygame
from os.path import join
from os import walk
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, bullet_group):
        super().__init__(groups)
        self.bullet_group = bullet_group

        # animation frames: keep originals (raw_frames) so scaling doesn't compound
        self.raw_frames = {'left': [], 'right': [], 'up': [], 'down': []}
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}
        self.load_images()

        self.state = 'down'
        self.frame_index = 0.0
        # if we have at least one image for down, use it; else create placeholder
        if self.frames['down']:
            self.image = self.frames['down'][0]
        else:
            self.image = pygame.Surface((32,32), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (0,0,255), self.image.get_rect(), 1)

        self.rect = self.image.get_rect(center=pos)

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 500

        # shooting
        self.shoot_cooldown = 0.25  # seconds
        self.time_since_last_shot = 0.0

        # health
        self.max_health = 5
        self.health = self.max_health
        self.invincible = True
        self.invincible_time = 2.0
        self.time_since_hit = -2.0

        self.damage = 1

        # scaling
        self.scale = 1.0

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()

        self.shoot(keys)

    def load_images(self):
        # load originals into raw_frames, then copy to frames
        base = join('images', 'player')
        for state in self.raw_frames.keys():
            folder = join(base, state)
            found = False
            for folder_path, _, file_names in walk(folder):
                if file_names:
                    found = True
                    for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                        surf = pygame.image.load(join(folder_path, file_name)).convert_alpha()
                        self.raw_frames[state].append(surf)
            if not found:
                # create a placeholder
                surf = pygame.Surface((32,32), pygame.SRCALPHA)
                pygame.draw.rect(surf, (255,0,0), surf.get_rect(), 1)
                self.raw_frames[state].append(surf)

        # copy raw_frames to frames (initial scale = 1)
        for state, flist in self.raw_frames.items():
            self.frames[state] = [s.copy() for s in flist]

    def set_scale(self, scale):
        # rescale frames based on raw_frames (so scaling is not cumulative)
        self.scale = scale
        for state, raw_list in self.raw_frames.items():
            new_list = []
            for surf in raw_list:
                w,h = surf.get_size()
                new_s = pygame.transform.scale(surf, (max(1, int(w*scale)), max(1, int(h*scale))))
                new_list.append(new_s)
            self.frames[state] = new_list
        # update current image and rect
        if self.frames[self.state]:
            self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
        else:
            self.image = pygame.Surface((int(32*scale), int(32*scale)), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.rect.center)

    def animate(self, dt):
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        # only animate when moving
        if self.direction.length_squared() > 0 and self.frames[self.state]:
            self.frame_index += 8 * dt
            idx = int(self.frame_index) % len(self.frames[self.state])
            self.image = self.frames[self.state][idx]
        else:
            # not moving -> show first frame
            self.frame_index = 0.0
            if self.frames[self.state]:
                self.image = self.frames[self.state][0]

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

        if direction and self.bullet_group is not None:
            Bullet(self.rect.center, direction, self.bullet_group)
            self.time_since_last_shot = 0.0

    def move(self, dt):
        new_pos = pygame.Vector2(self.rect.center) + self.direction * self.speed * dt
        self.rect.center = (int(new_pos.x), int(new_pos.y))

    def take_damage(self):
        if not self.invincible:
            self.health -= 1
            self.invincible = True
            self.time_since_hit = 0.0
            if self.health <= 0:
                print("Game Over!")

    def update(self, dt):
        self.dt = dt
        self.input()
        self.move(dt)
        self.animate(dt)

        if self.invincible:
            self.time_since_hit += dt
            if self.time_since_hit > self.invincible_time:
                self.invincible = False
